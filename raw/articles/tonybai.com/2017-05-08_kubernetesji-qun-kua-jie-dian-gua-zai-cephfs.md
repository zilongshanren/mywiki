---
title: Kubernetes集群跨节点挂载CephFS
url: https://tonybai.com/2017/05/08/mount-cephfs-acrossing-nodes-in-kubernetes-cluster/
published: '2017-05-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes集群跨节点挂载CephFS

在[Kubernetes](http://tonybai.com/tag/kubernetes)集群中运行有状态服务或应用总是不那么容易的。比如，之前我在项目中使用了[CephRBD](http://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd/)，虽然[遇到过几次问题](http://tonybai.com/2017/02/17/temp-fix-for-pod-unable-mount-cephrbd-volume/)，但总体算是运行良好。但最近发现CephRBD无法满足跨节点挂载的需求，我只好另辟蹊径。由于CephFS和CephRBD师出同门，它自然成为了这次我首要考察的目标。这里将跨节点挂载CephFS的考察过程记录一下，一是备忘，二则也可以为其他有相似需求的朋友提供些资料。

## 一、CephRBD的问题

这里先提一嘴CephRBD的问题。最近项目中有这样的需求：让集群中的Pod共享外部分布式存储，即多个Pod共同挂载一份存储，实现存储共享，这样可大大简化系统设计和复杂性。之前CephRBD都是挂载到一个Pod中运行的，CephRBD是否支持多Pod同时挂载呢？[官方文档](https://kubernetes.io/docs/concepts/storage/persistent-volumes)中给出了否定的答案: 基于CephRBD的Persistent Volume仅支持两种accessmode：

ReadWriteOnce和ReadOnlyMany，不支持ReadWriteMany。这样对于有读写需求的Pod来说，一个CephRBD pv仅能被一个node挂载一次。

我们来验证一下这个“不幸的”事实。

我们首先创建一个测试用的image：foo1。这里我利用了项目里写的[CephRBD API](http://tonybai.com/2016/11/21/kuberize-ceph-rbd-api-service/)服务，也可通过ceph命令手工创建：

```
# curl -v -H "Content-type: application/json" -X POST -d '{"kind": "Images","apiVersion": "v1", "metadata": {"name": "foo1", "capacity": 512} ' http://192.168.3.22:8080/api/v1/pools/rbd/images
... ...
{
"errcode": 0,
"errmsg": "ok"
}
# curl http://192.168.3.22:8080/api/v1/pools/rbd/images
{
"Kind": "ImagesList",
"APIVersion": "v1",
"Items": [
{
"name": "foo1"
}
]
}
```


利用下面文件创建pv和pvc：

```
//ceph-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
name: foo-pv
spec:
capacity:
storage: 512Mi
accessModes:
- ReadWriteMany
rbd:
monitors:
- ceph_monitor_ip:port
pool: rbd
image: foo1
user: admin
secretRef:
name: ceph-secret
fsType: ext4
readOnly: false
persistentVolumeReclaimPolicy: Recycle
//ceph-pvc.yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
name: foo-claim
spec:
accessModes:
- ReadWriteMany
resources:
requests:
storage: 512Mi
```


创建后：

```
# kubectl get pv
[NAME CAPACITY ACCESSMODES RECLAIMPOLICY STATUS CLAIM REASON AGE
foo-pv 512Mi RWO Recycle Bound default/foo-claim 20h
# kubectl get pvc
NAME STATUS VOLUME CAPACITY ACCESSMODES AGE
foo-claim Bound foo-pv 512Mi RWO 20h
```


创建挂载上述image的Pod：

```
// ceph-pod2.yaml
apiVersion: v1
kind: Pod
metadata:
name: ceph-pod2
spec:
containers:
- name: ceph-ubuntu2
image: ubuntu:14.04
command: ["tail", "-f", "/var/log/bootstrap.log"]
volumeMounts:
- name: ceph-vol2
mountPath: /mnt/cephrbd/data
readOnly: false
volumes:
- name: ceph-vol2
persistentVolumeClaim:
claimName: foo-claim
```


创建成功后，我们可以查看挂载目录的数据：

```
# kubectl exec ceph-pod2 ls /mnt/cephrbd/data
1.txt
lost+found
```


我们在同一个kubernetes node上再启动一个pod（可以把上面的ceph-pod2.yaml的pod name改为ceph-pod3），挂载同样的pv：

```
NAMESPACE NAME READY STATUS RESTARTS AGE IP NODE
default ceph-pod2 1/1 Running 0 3m 172.16.57.9 xx.xx.xx.xx
default ceph-pod3 1/1 Running 0 0s 172.16.57.10 xx.xx.xx.xx
```


```
# kubectl exec ceph-pod3 ls /mnt/cephrbd/data
1.txt
lost+found
```


我们通过ceph-pod2写一个文件，在ceph-pod3中将其读出：

```
# kubectl exec ceph-pod2 -- bash -c "for i in {1..10}; do sleep 1; echo 'pod2: Hello, World'>> /mnt/cephrbd/data/foo.txt ; done "
root@node1:~/k8stest/k8s-cephrbd/footest# kubectl exec ceph-pod3 cat /mnt/cephrbd/data/foo.txt
pod2: Hello, World
pod2: Hello, World
pod2: Hello, World
pod2: Hello, World
pod2: Hello, World
pod2: Hello, World
pod2: Hello, World
pod2: Hello, World
pod2: Hello, World
pod2: Hello, World
```


到目前为止，在一个node上多个Pod是可以以ReadWrite模式挂载同一个CephRBD的。

我们在另外一个节点启动一个试图挂载该pv的Pod，该Pod启动后一直处于pending状态，通过kubectl describe查看其详细信息，可以看到：

```
Events:
FirstSeen LastSeen Count From SubobjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
.. ...
2m 37s 2 {kubelet yy.yy.yy.yy} Warning FailedMount Unable to mount volumes for pod "ceph-pod2-master_default(a45f62aa-2bc3-11e7-9baa-00163e1625a9)": timeout expired waiting for volumes to attach/mount for pod "ceph-pod2-master"/"default". list of unattached/unmounted volumes=[ceph-vol2]
2m 37s 2 {kubelet yy.yy.yy.yy} Warning FailedSync Error syncing pod, skipping: timeout expired waiting for volumes to attach/mount for pod "ceph-pod2-master"/"default". list of unattached/unmounted volumes=[ceph-vol2]
```


查看kubelet.log中的错误日志：

```
I0428 11:39:15.737729 1241 reconciler.go:294] MountVolume operation started for volume "kubernetes.io/rbd/a45f62aa-2bc3-11e7-9baa-00163e1625a9-foo-pv" (spec.Name: "foo-pv") to pod "a45f62aa-2bc3-11e7-9baa-00163e1625a9" (UID: "a45f62aa-2bc3-11e7-9baa-00163e1625a9").
I0428 11:39:15.939183 1241 operation_executor.go:768] MountVolume.SetUp succeeded for volume "kubernetes.io/secret/923700ff-12c2-11e7-9baa-00163e1625a9-default-token-40z0x" (spec.Name: "default-token-40z0x") pod "923700ff-12c2-11e7-9baa-00163e1625a9" (UID: "923700ff-12c2-11e7-9baa-00163e1625a9").
E0428 11:39:17.039656 1241 disk_manager.go:56] failed to attach disk
E0428 11:39:17.039722 1241 rbd.go:228] rbd: failed to setup mount /var/lib/kubelet/pods/a45f62aa-2bc3-11e7-9baa-00163e1625a9/volumes/kubernetes.io~rbd/foo-pv rbd: image foo1 is locked by other nodes
E0428 11:39:17.039857 1241 nestedpendingoperations.go:254] Operation for "\"kubernetes.io/rbd/a45f62aa-2bc3-11e7-9baa-00163e1625a9-foo-pv\" (\"a45f62aa-2bc3-11e7-9baa-00163e1625a9\")" failed. No retries permitted until 2017-04-28 11:41:17.039803969 +0800 CST (durationBeforeRetry 2m0s). Error: MountVolume.SetUp failed for volume "kubernetes.io/rbd/a45f62aa-2bc3-11e7-9baa-00163e1625a9-foo-pv" (spec.Name: "foo-pv") pod "a45f62aa-2bc3-11e7-9baa-00163e1625a9" (UID: "a45f62aa-2bc3-11e7-9baa-00163e1625a9") with: rbd: image foo1 is locked by other nodes
```


可以看到“rbd: image foo1 is locked by other nodes”的日志。我们用试验证明了目前CephRBD仅能被k8s中的一个node挂载的事实。

## 二、Ceph集群安装mds以支持CephFS

这次我在两个Ubuntu 16.04的vm上新部署了一套Ceph，过程与之前[第一次部署Ceph](http://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd/)时大同小异，这里就不赘述了。要让Ceph支持CephFS，我们需要安装mds组件，有了前面的基础，通过ceph-deploy工具安装mds十分简单：

```
# ceph-deploy mds create yypdmaster yypdnode
[ceph_deploy.conf][DEBUG ] found configuration file at: /root/.cephdeploy.conf
[ceph_deploy.cli][INFO ] Invoked (1.5.37): /usr/bin/ceph-deploy mds create yypdmaster yypdnode
[ceph_deploy.cli][INFO ] ceph-deploy options:
[ceph_deploy.cli][INFO ] username : None
[ceph_deploy.cli][INFO ] verbose : False
[ceph_deploy.cli][INFO ] overwrite_conf : False
[ceph_deploy.cli][INFO ] subcommand : create
[ceph_deploy.cli][INFO ] quiet : False
[ceph_deploy.cli][INFO ] cd_conf : <ceph_deploy.conf.cephdeploy.Conf instance at 0x7f60fb5e71b8>
[ceph_deploy.cli][INFO ] cluster : ceph
[ceph_deploy.cli][INFO ] func : <function mds at 0x7f60fba4e140>
[ceph_deploy.cli][INFO ] ceph_conf : None
[ceph_deploy.cli][INFO ] mds : [('yypdmaster', 'yypdmaster'), ('yypdnode', 'yypdnode')]
[ceph_deploy.cli][INFO ] default_release : False
[ceph_deploy.mds][DEBUG ] Deploying mds, cluster ceph hosts yypdmaster:yypdmaster yypdnode:yypdnode
[yypdmaster][DEBUG ] connected to host: yypdmaster
[yypdmaster][DEBUG ] detect platform information from remote host
[yypdmaster][DEBUG ] detect machine type
[ceph_deploy.mds][INFO ] Distro info: Ubuntu 16.04 xenial
[ceph_deploy.mds][DEBUG ] remote host will use systemd
[ceph_deploy.mds][DEBUG ] deploying mds bootstrap to yypdmaster
[yypdmaster][DEBUG ] write cluster configuration to /etc/ceph/{cluster}.conf
[yypdmaster][DEBUG ] create path if it doesn't exist
[yypdmaster][INFO ] Running command: ceph --cluster ceph --name client.bootstrap-mds --keyring /var/lib/ceph/bootstrap-mds/ceph.keyring auth get-or-create mds.yypdmaster osd allow rwx mds allow mon allow profile mds -o /var/lib/ceph/mds/ceph-yypdmaster/keyring
[yypdmaster][INFO ] Running command: systemctl enable ceph-mds@yypdmaster
[yypdmaster][WARNIN] Created symlink from /etc/systemd/system/ceph-mds.target.wants/ceph-mds@yypdmaster.service to /lib/systemd/system/ceph-mds@.service.
[yypdmaster][INFO ] Running command: systemctl start ceph-mds@yypdmaster
[yypdmaster][INFO ] Running command: systemctl enable ceph.target
[yypdnode][DEBUG ] connected to host: yypdnode
[yypdnode][DEBUG ] detect platform information from remote host
[yypdnode][DEBUG ] detect machine type
[ceph_deploy.mds][INFO ] Distro info: Ubuntu 16.04 xenial
[ceph_deploy.mds][DEBUG ] remote host will use systemd
[ceph_deploy.mds][DEBUG ] deploying mds bootstrap to yypdnode
[yypdnode][DEBUG ] write cluster configuration to /etc/ceph/{cluster}.conf
[yypdnode][DEBUG ] create path if it doesn't exist
[yypdnode][INFO ] Running command: ceph --cluster ceph --name client.bootstrap-mds --keyring /var/lib/ceph/bootstrap-mds/ceph.keyring auth get-or-create mds.yypdnode osd allow rwx mds allow mon allow profile mds -o /var/lib/ceph/mds/ceph-yypdnode/keyring
[yypdnode][INFO ] Running command: systemctl enable ceph-mds@yypdnode
[yypdnode][WARNIN] Created symlink from /etc/systemd/system/ceph-mds.target.wants/ceph-mds@yypdnode.service to /lib/systemd/system/ceph-mds@.service.
[yypdnode][INFO ] Running command: systemctl start ceph-mds@yypdnode
[yypdnode][INFO ] Running command: systemctl enable ceph.target
```


非常顺利。安装后，可以在任意一个node上看到mds在运行：

```
# ps -ef|grep ceph
ceph 7967 1 0 17:23 ? 00:00:00 /usr/bin/ceph-osd -f --cluster ceph --id 1 --setuser ceph --setgroup ceph
ceph 15674 1 0 17:32 ? 00:00:00 /usr/bin/ceph-mon -f --cluster ceph --id yypdnode --setuser ceph --setgroup ceph
ceph 18019 1 0 17:35 ? 00:00:00 /usr/bin/ceph-mds -f --cluster ceph --id yypdnode --setuser ceph --setgroup ceph
```


mds是存储cephfs的元信息的，我的ceph是10.2.7版本：

```
# ceph -v
ceph version 10.2.7 (50e863e0f4bc8f4b9e31156de690d765af245185)
```


虽然支持多 active mds并行运行，但官方文档建议保持一个active mds，其他mds作为standby(见下面ceph集群信息中的fsmap部分)：

```
# ceph -s
cluster ffac3489-d678-4caf-ada2-3dd0743158b6
... ...
fsmap e6: 1/1/1 up {0=yypdnode=up:active}, 1 up:standby
osdmap e19: 2 osds: 2 up, 2 in
flags sortbitwise,require_jewel_osds
pgmap v192498: 576 pgs, 5 pools, 126 MB data, 238 objects
44365 MB used, 31881 MB / 80374 MB avail
576 active+clean
```


## 三、创建fs并测试挂载

我们在ceph上创建一个fs：

```
# ceph osd pool create cephfs_data 128
pool 'cephfs_data' created
# ceph osd pool create cephfs_metadata 128
pool 'cephfs_metadata' created
# ceph fs new test_fs cephfs_metadata cephfs_data
new fs with metadata pool 2 and data pool 1
# ceph fs ls
name: test_fs, metadata pool: cephfs_metadata, data pools: [cephfs_data ]
```


不过，ceph当前正式版功能中仅支持一个fs，对多个fs的支持仅存在于实验feature中：

```
# ceph osd pool create cephfs1_data 128
# ceph osd pool create cephfs1_metadata 128
# ceph fs new test_fs1 cephfs1_metadata cephfs1_data
Error EINVAL: Creation of multiple filesystems is disabled. To enable this experimental feature, use 'ceph fs flag set enable_multiple true'
```


在物理机上挂载cephfs可以使用mount命令、mount.ceph(apt-get install ceph-fs-common)或ceph-fuse(apt-get install ceph-fuse)，我们先用mount命令挂载：

```
我们将上面创建的cephfs挂载到主机的/mnt下：
#mount -t ceph ceph_mon_host:6789:/ /mnt -o name=admin,secretfile=admin.secret
# cat admin.secret //ceph.client.admin.keyring中的key
AQDITghZD+c/DhAArOiWWQqyMAkMJbWmHaxjgQ==
```


查看cephfs信息：

```
# df -h
ceph_mon_host:6789:/ 79G 45G 35G 57% /mnt
```


可以看出：cephfs将两个物理节点上的磁盘全部空间作为了自己的空间。

通过ceph-fuse挂载，还可以限制对挂载路径的访问权限，我们来创建用户foo，让其仅仅拥有对/ceph-volume1-test路径具有只读访问权限：

```
# ceph auth get-or-create client.foo mon 'allow *' mds 'allow r path=/ceph-volume1-test' osd 'allow *'
# ceph-fuse -n client.foo -m 10.47.217.91:6789 /mnt -r /ceph-volume1-test
ceph-fuse[10565]: starting ceph client2017-05-03 16:07:25.958903 7f1a14fbff00 -1 init, newargv = 0x557e350defc0 newargc=11
ceph-fuse[10565]: starting fuse
```


查看挂载路径，并尝试创建文件：

```
# cd /mnt
root@yypdnode:/mnt# ls
1.txt
root@yypdnode:/mnt# touch 2.txt
touch: cannot touch '2.txt': Permission denied
```


由于foo用户只拥有对 /ceph-volume1-test的只读权限，因此创建文件失败了！

## 四、Kubernetes跨节点挂载CephFS

在K8s中，至少可以通过两种方式挂载CephFS，一种是通过Pod直接挂载；另外一种则是通过pv和pvc挂载。我们分别来看。

### 1、Pod直接挂载CephFS

```
//ceph-pod2-with-secret.yaml
apiVersion: v1
kind: Pod
metadata:
name: ceph-pod2-with-secret
spec:
containers:
- name: ceph-ubuntu2
image: ubuntu:14.04
command: ["tail", "-f", "/var/log/bootstrap.log"]
volumeMounts:
- name: ceph-vol2
mountPath: /mnt/cephfs/data
readOnly: false
volumes:
- name: ceph-vol2
cephfs:
monitors:
- ceph_mon_host:6789
user: admin
secretFile: "/etc/ceph/admin.secret"
readOnly: false
```


注意：保证每个节点上都存在/etc/ceph/admin.secret文件。

查看Pod挂载的内容：

```
# docker ps|grep pod
bc96431408c7 ubuntu:14.04 "tail -f /var/log/boo" About a minute ago Up About a minute k8s_ceph-ubuntu2.66c44128_ceph-pod2-with-secret_default_3d8a05f8-33c3-11e7-bcd9-6640d35a0e90_fc483b8a
bcc65ab82069 gcr.io/google_containers/pause-amd64:3.0 "/pause" About a minute ago Up About a minute k8s_POD.d8dbe16c_ceph-pod2-with-secret_default_3d8a05f8-33c3-11e7-bcd9-6640d35a0e90_02381204
root@yypdnode:~# docker exec bc96431408c7 ls /mnt/cephfs/data
1.txt
apps
ceph-volume1-test
test1.txt
```


我们再在另外一个node上启动挂载同一个cephfs的Pod，看是否可以跨节点挂载：

```
# kubectl get pods
NAMESPACE NAME READY STATUS RESTARTS AGE IP NODE
default ceph-pod2-with-secret 1/1 Running 0 3m 172.30.192.2 iz2ze39jeyizepdxhwqci6z
default ceph-pod2-with-secret-on-master 1/1 Running 0 3s 172.30.0.51 iz25beglnhtz
... ...
# kubectl exec ceph-pod2-with-secret-on-master ls /mnt/cephfs/data
1.txt
apps
ceph-volume1-test
test1.txt
```


可以看到不同节点可以挂载同一CephFS。我们在一个pod中操作一下挂载的cephfs：

```
# kubectl exec ceph-pod2-with-secret-on-master -- bash -c "for i in {1..10}; do sleep 1; echo 'pod2-with-secret-on-master: Hello, World'>> /mnt/cephfs/data/foo.txt ; done "
root@yypdmaster:~/k8stest/cephfstest/footest# kubectl exec ceph-pod2-with-secret-on-master cat /mnt/cephfs/data/foo.txt
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
```


### 2、通过PV和PVC挂载CephFS

挂载cephfs的pv和pvc在写法方面与上面挂载rbd的类似：

```
//ceph-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
name: foo-pv
spec:
capacity:
storage: 512Mi
accessModes:
- ReadWriteMany
cephfs:
monitors:
- ceph_mon_host:6789
path: /
user: admin
secretRef:
name: ceph-secret
readOnly: false
persistentVolumeReclaimPolicy: Recycle
//ceph-pvc.yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
name: foo-claim
spec:
accessModes:
- ReadWriteMany
resources:
requests:
storage: 512Mi
```


使用pvc的pod:

```
//ceph-pod2.yaml
apiVersion: v1
kind: Pod
metadata:
name: ceph-pod2
spec:
containers:
- name: ceph-ubuntu2
image: ubuntu:14.04
command: ["tail", "-f", "/var/log/bootstrap.log"]
volumeMounts:
- name: ceph-vol2
mountPath: /mnt/cephfs/data
readOnly: false
volumes:
- name: ceph-vol2
persistentVolumeClaim:
claimName: foo-claim
```


创建pv、pvc：

```
# kubectl create -f ceph-pv.yaml
persistentvolume "foo-pv" created
# kubectl create -f ceph-pvc.yaml
persistentvolumeclaim "foo-claim" created
# kubectl get pvc
NAME STATUS VOLUME CAPACITY ACCESSMODES AGE
foo-claim Bound foo-pv 512Mi RWX 4s
# kubectl get pv
NAME CAPACITY ACCESSMODES RECLAIMPOLICY STATUS CLAIM REASON AGE
foo-pv 512Mi RWX Recycle Bound default/foo-claim 24s
```


启动pod，通过exec命令查看挂载情况：

```
# docker ps|grep pod
a6895ec0274f ubuntu:14.04 "tail -f /var/log/boo" About a minute ago Up About a minute k8s_ceph-ubuntu2.66c44128_ceph-pod2_default_4e4fc8d4-33c6-11e7-bcd9-6640d35a0e90_1b37ed76
52b6811a6584 gcr.io/google_containers/pause-amd64:3.0 "/pause" About a minute ago Up About a minute k8s_POD.d8dbe16c_ceph-pod2_default_4e4fc8d4-33c6-11e7-bcd9-6640d35a0e90_27e5f988
55b96edbf4bf ubuntu:14.04 "tail -f /var/log/boo" 14 minutes ago Up 14 minutes k8s_ceph-ubuntu2.66c44128_ceph-pod2-with-secret_default_9d383b0c-33c4-11e7-bcd9-6640d35a0e90_1656e5e0
f8b699bc0459 gcr.io/google_containers/pause-amd64:3.0 "/pause" 14 minutes ago Up 14 minutes k8s_POD.d8dbe16c_ceph-pod2-with-secret_default_9d383b0c-33c4-11e7-bcd9-6640d35a0e90_effdfae7
root@yypdnode:~# docker exec a6895ec0274f ls /mnt/cephfs/data
1.txt
apps
ceph-volume1-test
foo.txt
test1.txt
# docker exec a6895ec0274f cat /mnt/cephfs/data/foo.txt
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
pod2-with-secret-on-master: Hello, World
```


## 五、pv的状态

如果你不删除pvc，一切都安然无事：

```
# kubectl get pv
NAME CAPACITY ACCESSMODES RECLAIMPOLICY STATUS CLAIM REASON AGE
foo-pv 512Mi RWX Recycle Bound default/foo-claim 1h
# kubectl get pvc
NAME STATUS VOLUME CAPACITY ACCESSMODES AGE
foo-claim Bound foo-pv 512Mi RWX 1h
```


但是如果删除pvc，pv的状态将变成failed：

```
删除pvc：
# kubectl get pv
NAME CAPACITY ACCESSMODES RECLAIMPOLICY STATUS CLAIM REASON AGE
foo-pv 512Mi RWX Recycle Failed default/foo-claim 2h
# kubectl describe pv/foo-pv
Name: foo-pv
Labels: <none>
Status: Failed
Claim: default/foo-claim
Reclaim Policy: Recycle
Access Modes: RWX
Capacity: 512Mi
Message: No recycler plugin found for the volume!
Source:
Type: RBD (a Rados Block Device mount on the host that shares a pod's lifetime)
CephMonitors: [xx.xx.xx.xx:6789]
RBDImage: foo1
FSType: ext4
RBDPool: rbd
RadosUser: admin
Keyring: /etc/ceph/keyring
SecretRef: &{ceph-secret}
ReadOnly: false
Events:
FirstSeen LastSeen Count From SubobjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
29s 29s 1 {persistentvolume-controller } Warning VolumeFailedRecycle No recycler plugin found for the volume!
```


我们在pv中指定的persistentVolumeReclaimPolicy是Recycle，但无论是cephrbd还是cephfs都不没有对应的recycler plugin，导致pv的status变成了failed，只能手工删除重建。

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

你好，写的文章真的不错，明白了块存储不支持跨节点。但是上面的 “之前CephRBD都是挂载到一个Pod中运行的，CephRBD是否支持多Pod同时挂载呢？官方文档中给出了否定的答案: 基于CephRBD的Persistent Volume仅支持两种accessmode：ReadWriteOnce和ReadOnlyMany，不支持ReadWriteMany。” 与下面的试验不同，其中pvc的accessModes:为 – ReadWriteMany。而且pod2和pod3都挂载上了rbd。不知是否是我理解有偏差

试验目的是验证”那个不幸的事实”：即 在不同node上多个Pod是无法以ReadWriteMany模式挂载同一个CephRBD的。同时试验也验证了：在一个node上多个Pod是可以以ReadWriteMany模式挂载同一个CephRBD的。另外这里有一个预制条件，我没提到，那就是我只考虑ReadWriteMany这种模式(所以仅验证了ReadWriteMany模式)，ReadWriteOnce和ReadOnlyMany对我的使用场景没有意义。

明白你的意思了。非常感谢！！

请教一下：ceph集群创建fs后，是不是一定要先挂载在ceph集群主机上呢，然后k8s再去挂载fs，这样数据就存储在ceph集群上了。如果ceph集群创建了fs，没有挂载在ceph集群上，k8s的pod直接去挂载fs，这样数据是不是不会存在ceph集群中。文章中的，三、创建fs并测试挂载 与 四、Kubernetes跨节点挂载CephFS 三也挂载了，四也是挂载，是先后顺序还是？

ceph集群创建fs后，不用先挂载到使用cephfs的k8s cluster的node上。k8s支持使用persistent volume和pv claim直接挂载cephfs。而k8s pods直接使用这些pvc即可。

嗯。那三，创建fs并测试挂载，这里的挂载是在做什么呢，是挂在ceph集群机子上吗？

创建fs后，通过主机挂载cephfs的方式测试一下创建的fs是否好用，这就是第三步骤的目的。一旦第三步创建的cephfs是好用的，第四步我们就要在K8s的pod中直接挂载cephfs了，而并不是通过挂载本地已经挂载到cephfs的目录的方式。

非常感谢这么认真的回复！已经实验过了，成功将数据存在了ceph集群中。还有一个问题，不知有没有用过k8s的动态存储，storageClass ,使用cephFS。

目前还没有使用过storageClass。

您好，咨询一个使用阿里云kubernetes挂载NFS的问题，我的问题如下：

https://github.com/kubernetes/kubernetes/issues/56735

我的NAS是创建成功的，可以挂载在node上，pv和pvc也是成功的，但就是pod在mount nas的时候timeout, 请问有什么解决方法吗？

nas也好，nfs也好，我都没有试过。不过你可以试试在某个node上本地（非pod）手工挂载nas能成功么？

大神，再请教一个问题：经过实验，ceph集群目前只可以创建一个fs，那么k8s要使用的话，所有的用户应用之类的都会存在一起，这样可能存在了冲突之类的，想请教下，如何进行隔离呢，有什么方法或者建议呢

按照ceph文档，jewel及之后发布版支持对挂载路径的读写修改限制，可以参考这个文档： http://docs.ceph.com/docs/kraken/cephfs/client-auth/ 不过之前记得测试过一次，似乎不大好用。不过我当时测试的ceph版本恰是10.2.3(jewel),也许还不完善。后来就没有进一步验证。不知道新版是否真正支持了该feature。

大神，你好。请问一下就是我现在使用pv挂在的话，我申请的是512Mi,pvc也是，为什么我pod挂在上确实磁盘总大小，就和pod直接挂载是一样的。

的确是这样的，我的环境挂载后看到的也是整个cephfs的整体空间。我没有细致研究过，我个人猜测：一个可能是插件实现的问题（又或可能是cephfs本身尚不支持划分磁盘大小）。另外一个可能是挂载的是cephfs，而不是cephrbd，cephfs目前整个ceph集群只能创建一个，cephfs视整个ceph集群节点上的磁盘全部空间为自己的空间。从挂载的pod的角度看cephfs，实则看到的是cephfs下面的那个ceph image的整体大小。

你好，问一下我本地测试可以通过，但是Pod测试的时候报错。

df -h

192.168.181.93:6789:/ 95G 0 95G 0% /mnt

kubectl describe pod ceph-pod2-with-secret

Mounting arguments: -t ceph -o name=admin,secretfile=/data/cephfs/admin.secret 192.168.181.93:6789:/ /var/lib/kubelet/pods/2af20094-89b3-11e8-a44a-000c29cc5e76/volumes/kubernetes.io~cephfs/ceph-vol2

Output: mount: wrong fs type, bad option, bad superblock on 192.168.181.93:6789:/,

missing codepage or helper program, or other error

In some cases useful info is found in syslog – try

dmesg | tail or so.

问一下，这是什么原因呢？

我没遇到过类似问题。不过k8s上的issue中有与你遇到的问题类似的issue，请参考这个解决：https://github.com/kubernetes/kubernetes/issues/39227

没有看明白啊，他说是由于 encoding的问题，但是我的.secret 文件就是utf8的 ，里边的内容是base64的。

你的每个k8s节点上都存在/etc/ceph/admin.secret文件? 另外出错时，dmesg | tail的输出是啥?

是，每个节点都有

dmesg

[232683.458167] EXT4-fs (rbd0): VFS: Can’t find ext4 filesystem

[232684.472345] EXT4-fs (rbd0): mounted filesystem with ordered data mode. Opts: (null)

[232688.634998] IPv6: ADDRCONF(NETDEV_UP): eth0: link is not ready

[232688.667143] IPv6: ADDRCONF(NETDEV_CHANGE): eth0: link becomes ready

[233056.592089] libceph: mon0 192.168.181.93:6789 session established

[233056.594443] libceph: client25404 fsid 20631ce0-4c16-4b5e-9f45-759943951a45

[233056.648198] rbd: rbd0: capacity 21474836480 features 0×1

[233057.064804] EXT4-fs (rbd0): mounted filesystem with ordered data mode. Opts: (null)

[233059.633525] IPv6: ADDRCONF(NETDEV_UP): eth0: link is not ready

[233059.633993] IPv6: ADDRCONF(NETDEV_CHANGE): eth0: link becomes ready

[234213.872978] systemd-journald[487]: Failed to set file attributes: Operation not supported

[234213.919069] systemd-journald[487]: Failed to set file attributes: Operation not supported

[236614.545464] systemd-journald[487]: Failed to set file attributes: Operation not supported

“EXT4-fs (rbd0): VFS: Can’t find ext4 filesystem” , 你的各个物理节点上使用文件系统是ext4么？

这是我的pod,请帮忙查看一下问题，谢谢

apiVersion: v1

kind: Pod

metadata:

name: ceph-pod2-with-secret

spec:

containers:

– name: ceph-ubuntu2

image: ubuntu:14.04

command: ["tail", "-f", "/var/log/bootstrap.log"]

volumeMounts:

– name: ceph-vol2

mountPath: /mnt/cephfs/data

readOnly: false

volumes:

– name: ceph-vol2

cephfs:

monitors:

– 192.168.181.93:6789

user: admin

secretFile: “/data/cephfs/admin.secret”

readOnly: false

~

dmesg

[232683.458167] EXT4-fs (rbd0): VFS: Can’t find ext4 filesystem

[232684.472345] EXT4-fs (rbd0): mounted filesystem with ordered data mode. Opts: (null)

[232688.634998] IPv6: ADDRCONF(NETDEV_UP): eth0: link is not ready

[232688.667143] IPv6: ADDRCONF(NETDEV_CHANGE): eth0: link becomes ready

[233056.592089] libceph: mon0 192.168.181.93:6789 session established

[233056.594443] libceph: client25404 fsid 20631ce0-4c16-4b5e-9f45-759943951a45

[233056.648198] rbd: rbd0: capacity 21474836480 features 0×1

[233057.064804] EXT4-fs (rbd0): mounted filesystem with ordered data mode. Opts: (null)

[233059.633525] IPv6: ADDRCONF(NETDEV_UP): eth0: link is not ready

[233059.633993] IPv6: ADDRCONF(NETDEV_CHANGE): eth0: link becomes ready

[234213.872978] systemd-journald[487]: Failed to set file attributes: Operation not supported

[234213.919069] systemd-journald[487]: Failed to set file attributes: Operation not supported

[236614.545464] systemd-journald[487]: Failed to set file attributes: Operation not supported

请教下,cephfs如果使用k8s挂载的话 如何限制挂载指定目录的大小呢?

没试过。不过建议参考一下：http://docs.ceph.com/docs/mimic/cephfs/quota 自己探索一下:)。不过cephfs的quota可能对操作系统内核版本、k8s版本有依赖。这篇文章有描述：https://www.cnblogs.com/ltxdzh/p/9173706.html 也可以参考一下。