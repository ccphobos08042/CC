

<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-button type="primary" @click="handleAdd">新增</a-button>
          <a-button @click="handleBatchDelete">批量删除</a-button>
        </a-space>
      </div>
      <a-table
          :columns="columns"
          :data-source="data.userList"
          :loading="data.loading"
          :pagination="{
          size: 'default',
          current: data.page,
          pageSize: data.pageSize,
          onChange: (current) => (data.page = current),
          showSizeChanger: false,
          showTotal: (total) => `共${total}条数据`,
        }"
          :row-selection="rowSelection"
          :scroll="{ x: 'max-content' }"
          rowKey="id"
          size="middle"
      >
        <template #bodyCell="{ text, record, index, column }">
          <template v-if="column.key === 'operation'">
            <span>
              <a @click="handleEdit(record)">编辑</a>
              <a-divider type="vertical"/>
              <a-popconfirm cancel-text="否" ok-text="是" title="确定删除?" @confirm="confirmDelete(record)">
                <a href="#">删除</a>
              </a-popconfirm>
            </span>
          </template>
        </template>
      </a-table>
    </div>

    <div>

      <a-modal
  :visible="itemModalState.visible"
  title="添加新物品"
  @ok="handleAddItem"
  @cancel="itemModalState.visible = false"
>
  <a-input
    v-model:value="itemModalState.newItemName"
    placeholder="请输入物品名称"
    @pressEnter="handleAddItem"
  />
</a-modal>
      <a-modal
          :footer="null"
          :visible="itemModal.visible"
          title="物品详情"
          @cancel="itemModal.visible = false"
      >
        <a-descriptions :column="2" bordered>
          <template v-for="(status, item) in itemModal.items" :key="item">
            <a-descriptions-item :label="item">
        <span :style="{
          color: status === 1 ? 'green' :
                 status === 0 ? '#ffcc00' :
                 'red'
        }">
          {{ status === 1 ? '未损坏' :
            status === 0 ? '缺失' :
                '异常' }}
        </span>

            </a-descriptions-item>
          </template>
        </a-descriptions>
      </a-modal>
      <a-modal
          :forceRender="true"
          :title="modal.title"
          :visible="modal.visile"
          cancel-text="取消"
          ok-text="确认"
          @cancel="handleCancel"
          @ok="handleOk"
      >
        <div>

          <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="modal.form" :rules="modal.rules">
            <a-row :gutter="24">
              <a-col span="24">
                <a-form-item label="编号" name="id">
                  <a-input-number v-if="!modal.editFlag"
                      v-model:value="modal.form.id"
                      :controls="false"
                      placeholder="请输入编号"
                      style="width: 100%"
                  />
                  <a-input-number disabled v-if="modal.editFlag"
                      v-model:value="modal.form.id"
                      :controls="false"
                      placeholder="请输入编号"
                      style="width: 100%"
                  />
                </a-form-item>
              </a-col>
              <a-col span="24">
                <img
                  v-if="modal.form.pic"
                  :src="modal.form.pic"
                  style="max-width: 100%; height: auto;"
                />
              </a-col>
                <a-col span="24">
                  <a-descriptions bordered :column="2">
                    <template v-for="(status, item) in modal.form.item ? JSON.parse(modal.form.item) : {}" :key="item">
                      <a-descriptions-item :label="item">
                        <span v-if="!modal.editFlag" :style="{
                          color: status === 1 ? 'green' :
                                 status === 0 ? '#ffcc00' :
                                 'red'
                        }" @click="status === 0 && confirmItemExists(item)">
                          {{ status === 1 ? '检测到' : '未检测到' }}
                        </span>
                        <span v-if="modal.editFlag" >
                          <a-button v-if="status===2" type="ghost" disabled>已报修</a-button>
                          <a-button v-if="status==1" type="primary" @click="baoxiu(item)" >报修</a-button>
                          <a-button v-if="status==0" type="primary" @click="lose(item)" >缺失</a-button>
                        </span>
                      </a-descriptions-item>
                    </template>
                  </a-descriptions>
                  <a-button
    v-if="modal.form.type === 2"
    type="dashed"
    @click="showAddItemModal"
    style="margin-top: 8px"
  >
    <plus-outlined /> 添加物品
  </a-button>
                </a-col>
              <a-col span="24">
                <a-form-item label="类型" name="type" >
                  <a-select disabled v-if="modal.editFlag"
                    v-model:value="modal.form.type"
                    placeholder="请选择类型"
                    style="width: 100%"
                    @change="handleTypeChange"
                  >
                    <a-select-option :value="0">小警具包</a-select-option>
                    <a-select-option :value="1">大警具包</a-select-option>
                    <a-select-option :value="2">自定义包</a-select-option>
                  </a-select>
                  <a-select v-if="!modal.editFlag"
                    v-model:value="modal.form.type"
                    placeholder="请选择类型"
                    style="width: 100%"
                    @change="handleTypeChange"
                  >
                    <a-select-option :value="0">小警具包</a-select-option>
                    <a-select-option :value="1">大警具包</a-select-option>
                    <a-select-option :value="2">自定义包</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="状态" name="status">
                  <a-select
                    v-model:value="modal.form.status"
                    placeholder="请选择状态"
                    style="width: 100%"
                  >
                    <a-select-option :value="0">报修</a-select-option>
                    <a-select-option :value="1">取出</a-select-option>
                    <a-select-option :value="2">可取</a-select-option>
                    <a-select-option :value="3">缺失</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="24">
  <a-form-item label="柜号" name="cabinet">
    <a-select
      v-model:value="modal.form.cabinet"
      placeholder="请选择柜号"
      style="width: 100%"
    >
      <a-select-option
        v-for="cabinetId in modal.cabinetList"
        :key="cabinetId"
        :value="cabinetId"
      >
        {{ cabinetId }}
      </a-select-option>
    </a-select>
  </a-form-item>
</a-col>


            </a-row>
          </a-form>
          <a-button type="primary" @click="yolov8" v-if="!modal.editFlag">检测</a-button>
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {FormInstance, message} from 'ant-design-vue';
import {createApi, listApi, updateApi, deleteApi,yolov8Api,baoxiuApi} from '/@/api/jingju';
import { Modal } from 'ant-design-vue';
import {listApi as jjglist} from '/@/api/jingjucabinet';
const columns = reactive([
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
  },
  {
    title: '类型',
    dataIndex: 'type',
    key: 'type',
    customRender: ({ text }) => {
      let typeText = '';
      switch (text) {
        case 1:
          typeText = '大警具包';
          break;
        case 0:
          typeText = '小警具包';
          break;
        default:
          typeText = '自定义包';
      }
      return h('span', typeText);
    }
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    customRender: ({ text }) => {
      let statusText = '';
      let color = '';
      switch (text) {
        case 1:
          statusText = '取出';
          color = '#ff6200'; // orange for borrowed
          break;
        case 2:
          statusText = '可取';
          color = '#52c41a'; // green for available
          break;
        case 0:
          statusText = '报修';
          color = '#ff0000'; // red for repair
          break;
        default:
          statusText = '缺失';
          color = '#8c8c8c'; // gray for unknown
      }
      return h('span', { style: { color } }, statusText);
    }
  },
  {
    title: '柜号',
    dataIndex: 'cabinet',
    key: 'cabinet',
  },

  {
    title: '物品',
    dataIndex: 'item',
    key: 'item',
    customRender: ({ text }) => {
      return h('a', { type: 'primary',onClick: () => showItemDetail(text) }, '查看');
    }
  },
  {
    title: '最后操作人',
    dataIndex: 'last_people',
    key: 'last_people',
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'operation',
    align: 'center',
    fixed: 'right',
    width: 140,
  },
]);

const showItemDetail = (items) => {
  try {
    itemModal.items = typeof items === 'string' ? JSON.parse(items) : items;
    itemModal.visible = true;
  } catch (e) {
    message.error('物品数据格式错误');
  }
};
const handleTypeChange = (value: number) => {
  if (value === 0) { // 如果选择了“小警具包”
    modal.form.item = JSON.stringify({"手铐":0,"匕首":0,"约束绳":0,"防割手套":0,"强光手电":0,"扎带":0});
  } else if (value === 1) { // 如果选择了“大警具包”
    modal.form.item = JSON.stringify({"手铐":0,"匕首":0,"约束绳":0,"防割手套":0,"强光手电":0,"扎带":0,"防刺背心":0,"伸缩棍":0});
    // 当选择其他类型时，可根据需要重置 item 字段

  }else {
    modal.form.item = JSON.stringify({});

  }
};
const itemModalState = reactive({
  visible: false,
  newItemName: ''
});
const showAddItemModal = () => {
  itemModalState.visible = true;
  itemModalState.newItemName = '';
};
const handleAddItem = () => {
  if (itemModalState.newItemName) {
    try {
      const currentItems = modal.form.item ? JSON.parse(modal.form.item) : {};
      currentItems[itemModalState.newItemName] = 0;
      modal.form.item = JSON.stringify(currentItems);
      itemModalState.visible = false;
    } catch (e) {
      message.error('添加物品失败');
    }
  }
};
const updateItemStatus = (form: any, item: string) => {
  const updatedForm = { ...form };
  if (updatedForm.item) {
    try {
      const itemData = JSON.parse(updatedForm.item);
      if (itemData.hasOwnProperty(item)) {
        itemData[item] = 1;
      }
      updatedForm.item = JSON.stringify(itemData);
    } catch (parseError) {
      console.error('Error parsing item data:', parseError);
      message.error('Failed to parse item data');
      return null;
    }
  }
  return updatedForm;
};
const confirmItemExists = (item: string) => {
  Modal.confirm({
    title: '是否已存在该物品？',
    content: '确认后该物品状态将转为检测到',
    onOk: () => {
      const updatedForm = updateItemStatus(modal.form, item);
      if (updatedForm) {
        modal.form = updatedForm;
        message.success('物品状态已更新为检测到');
      }
    },
    onCancel: () => {
      // Do nothing when cancel
    },
  });
};
import {useUserStore} from "/@/store";
const userStore = useUserStore();
const baoxiu = async (item: string) => {
  Modal.confirm({
    title: '确认操作',
    content: '是否报修？',
    onOk: async () => {
      try {
        const params = {
      wupin: item,
      guanhao: modal.form.cabinet,
      baohao: modal.form.id,
      baoxiuren: userStore.admin_user_name,
      zhuangtai: 0
    };

    // 调用报修接口
    const res = await baoxiuApi(params);
    message.success('报修成功');
    console.log('报修请求成功', res);
        // 克隆 modal.form 对象，避免直接修改原始对象
        const updatedForm = { ...modal.form };

        // 解析 item 数据
        if (updatedForm.item) {
          const itemData = JSON.parse(updatedForm.item);

          // 将传入的 item 对应的值改为 2
          if (itemData.hasOwnProperty(item)) {
            itemData[item] = 2;
          }

          // 检查 item 状态并设置 status
          const hasZero = Object.values(itemData).includes(0);
          const hasTwo = Object.values(itemData).includes(2);

          if (!hasZero && !hasTwo) {
            updatedForm.status = 2; // 所有项为1
          } else if (hasZero) {
            updatedForm.status = 3; // 存在0
          } else if (hasTwo) {
            updatedForm.status = 0; // 存在2
          }

          // 将更新后的 item 数据重新转换为 JSON 字符串
          updatedForm.item = JSON.stringify(itemData);
        }

        // 调用更新接口
        await updateApi({ id: modal.form.id }, updatedForm);
        message.success('信息更新成功');
        console.log('更新请求成功');
        modal.form = updatedForm;
        getDataList(); // 刷新数据列表
      } catch (error) {
        message.error('操作失败' + error);
        console.error('操作失败', error);
      }
    },
    onCancel: () => {
      // 用户取消操作时不执行任何操作
    },
  });
};

// ... existing code ...
const lose = async (item: string) => {
  Modal.confirm({
    title: '确认操作',
    content: '是否将物品状态改为已有？',
    onOk: async () => {
      try {
        // 克隆 modal.form 对象，避免直接修改原始对象
        const updatedForm = { ...modal.form };

        // 解析 item 数据
        if (updatedForm.item) {
          const itemData = JSON.parse(updatedForm.item);

          // 将传入的 item 对应的值改为 1
          if (itemData.hasOwnProperty(item)) {
            itemData[item] = 1;
          }

          // 检查 item 状态并设置 status
          const hasZero = Object.values(itemData).includes(0);
          const hasTwo = Object.values(itemData).includes(2);

          if (!hasZero && !hasTwo) {
            updatedForm.status = 2; // 所有项为1
          } else if (hasZero) {
            updatedForm.status = 3; // 存在0
          } else if (hasTwo) {
            updatedForm.status = 0; // 存在2
          }

          // 将更新后的 item 数据重新转换为 JSON 字符串
          updatedForm.item = JSON.stringify(itemData);
        }

        // 调用更新接口
        await updateApi({ id: modal.form.id }, updatedForm);
        message.success('信息更新成功');
        console.log('更新请求成功');
        modal.form = updatedForm;
        getDataList(); // 刷新数据列表
      } catch (error) {
        message.error('操作失败' + error);
        console.error('操作失败', error);
      }
    },
    onCancel: () => {
      // 用户取消操作时不执行任何操作
    },
  });
};
// ... existing code ...
/*
const yolov8 = async () => {
  try {
    // 获取视频流
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    const video = document.createElement('video');
    video.srcObject = stream;
    await video.play();

    // 创建canvas
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');

    // 定义拍照函数
    const takePhoto = () => {
      ctx?.drawImage(video, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL('image/jpeg', 0.9);
    };

    // 连拍20张照片
    let lastPhoto = '';
    for (let i = 0; i < 20; i++) {
      lastPhoto = takePhoto();
      await new Promise(resolve => setTimeout(resolve, 100)); // 每张照片间隔100ms
    }

    // 停止视频流
    stream.getTracks().forEach(track => track.stop());

    // 调用yolov8Api接口，使用最后一张照片
    const result = await yolov8Api({ image: lastPhoto });
    let itemdata=JSON.stringify(result.data["data"])
    let pic='data:image/jpeg;base64,'+result.data["img"]
    modal.form = {
      ...modal.form,
      id: modal.form.id,
      pic:pic || modal.form.pic,
      item: itemdata|| modal.form.item,
      type: modal.form.type,
      status: modal.form.status,
      cabinet: modal.form.cabinet,
      last_people: modal.form.last_people
    };


  } catch (error) {
    console.error('Error accessing camera:', error);
    message.error("检测失败"+error);
  }
};

*/
const yolov8 = async () => {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(device => device.kind === 'videoinput');

    if (videoDevices.length === 0) {
      throw new Error('没有找到摄像头设备');
    }

    // 如果有多个摄像头，让用户选择
    let deviceId;
    if (videoDevices.length > 1) {
      // 这里可以改成更友好的UI选择方式
      const selected = confirm(`检测到 ${videoDevices.length} 个摄像头，是否使用1号摄像头\n`);
      deviceId = selected ? videoDevices[0].deviceId : videoDevices[1].deviceId;
    } else {
      deviceId = videoDevices[0].deviceId;
    }
    // 获取视频流
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true
    });
    const video = document.createElement('video');
    video.srcObject = stream;
    await video.play();

    // 创建 canvas
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');

    // 定义拍照函数
    const takePhoto = () => {
      ctx?.drawImage(video, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL('image/jpeg', 0.9);
    };

    // 连拍 20 张照片
    let lastPhoto = '';
    for (let i = 0; i < 20; i++) {
      lastPhoto = takePhoto();
      await new Promise(resolve => setTimeout(resolve, 100)); // 每张照片间隔 100ms
    }

    // 停止视频流
    stream.getTracks().forEach(track => track.stop());

    // 调用 yolov8Api 接口，使用最后一张照片
    const result = await yolov8Api({ image: lastPhoto });
    let resultData = result.data["data"];
    let pic = 'data:image/jpeg;base64,' + result.data["img"];

    // 解析原始物品数据
    let originalItemData = {};
    if (modal.form.item) {
      try {
        originalItemData = JSON.parse(modal.form.item);
      } catch (e) {
        console.error('解析原始物品数据时出错:', e);
      }
    }

    // 检查相同键并更新值
    for (let key in resultData) {
      if (originalItemData.hasOwnProperty(key)) {
        originalItemData[key] = 1;
      }
    }

    // 更新表单数据
    modal.form = {
      ...modal.form,
      pic: pic || modal.form.pic,
      item: JSON.stringify(originalItemData) || modal.form.item,
    };

  } catch (error) {
    console.error('访问摄像头出错:', error);
    message.error("检测失败" + error);
  }
};

// ... 已有代码 ...
// 页面数据
const data = reactive({
  userList: [],
  loading: false,
  currentAdminUserName: '',
  keyword: '',
  selectedRowKeys: [] as any[],
  pageSize: 10,
  page: 1,
});

// 弹窗数据源
const modal = reactive({
  visile: false,
  editFlag: false,
  title: '',
  cabinetList: [] as string[],
  form: {
    pic:undefined,
    id: undefined,
    item: undefined,
    type: undefined,
    status: undefined,
    cabinet: undefined,
    last_people: undefined,
  },
});
const itemModal = reactive({
  visible: false,
  items: {} as Record<string, number>
});
const myform = ref<FormInstance>();

onMounted(() => {
  getDataList();
});

const getDataList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
    page: data.page,
    pageSize: data.pageSize
  })
      .then((res) => {
        data.loading = false;
        console.log(res);
        // 处理返回的数据
        data.userList = res.data.map((item: any) => {
          return {
            ...item,
            // 如果需要特殊处理某些字段可以在这里进行
            item: JSON.stringify(item.item) // 将JSON字段转换为字符串显示
          };
        });
      })
      .catch((err) => {
        data.loading = false;
        console.log(err);
        message.error('获取数据失败');
      });
};

const rowSelection = ref({
  onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
    console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    data.selectedRowKeys = selectedRowKeys;
  },
});

const handleAdd = () => {
  resetModal();
  modal.visile = true;
  modal.editFlag = false;
  modal.title = '新增';
  jjglist().then(res => {
    modal.cabinetList = res.data.map((cabinet: any) => cabinet.id); // 假设接口返回柜号字段为id
  }).catch(err => {
    message.error('获取警具柜列表失败');
  });
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
  modal.form.status = 2;
};
const handleEdit = (record: any) => {
  resetModal();
  modal.visile = true;
  modal.editFlag = true;
  modal.title = '编辑';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
  for (const key in record) {
    modal.form[key] = record[key];
  }

};

const confirmDelete = (record: any) => {
  console.log('delete', record);
  deleteApi({ids: record.id})
      .then((res) => {
        getDataList();
      })
      .catch((err) => {
        message.error(err.msg || '删除失败');
      });
};

const handleBatchDelete = () => {
  console.log(data.selectedRowKeys);
  if (data.selectedRowKeys.length <= 0) {
    console.log('hello');
    message.warn('请勾选删除项');
    return;
  }
  deleteApi({ids: data.selectedRowKeys.join(',')})
      .then((res) => {
        message.success('删除成功');
        data.selectedRowKeys = [];
        getDataList();
      })
      .catch((err) => {
        message.error(err.msg || '删除失败');
      });
};

const handleOk = () => {
  // 自动存储当前用户 ID
  modal.form.last_people = "admin";
  if (!modal.editFlag && modal.form.item) {
    try {
      const itemData = JSON.parse(modal.form.item);
      const allItemsValid = Object.values(itemData).every(val => val === 1);
      modal.form.status = allItemsValid ? 2 : 3;
    } catch (e) {
      console.error('解析item数据时出错:', e);
      message.error('物品数据格式错误');
      return;
    }
  }
  const formData = { ...modal.form };
  delete formData.pic;
  myform.value
      ?.validate()
      .then(() => {
        if (modal.editFlag) {
          updateApi({id: modal.form.id}, modal.form)
              .then((res) => {
                hideModal();
                getDataList();
              })
              .catch((err) => {
                console.log(err);
                message.error(err.msg || '操作失败');
              });
        } else {
          createApi(modal.form)
              .then((res) => {
                hideModal();
                getDataList();
              })
              .catch((err) => {
                console.log(err);
                message.error(err.msg || '操作失败');
              });
        }
      })
      .catch((err) => {
        console.log('不能为空');
      });
};


const handleCancel = () => {
  hideModal();
};

// 恢复表单初始状态
const resetModal = () => {
  myform.value?.resetFields();
};

// 关闭弹窗
const hideModal = () => {
  modal.visile = false;
};
</script>

<style lang="less" scoped>
.page-view {
  min-height: 100%;
  background: #fff;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.table-operations {
  margin-bottom: 16px;
  text-align: right;
}

.table-operations > button {
  margin-right: 8px;
}
</style>
