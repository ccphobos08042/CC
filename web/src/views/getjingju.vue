<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">

        <a-space>
          <a>您当前的领取权限:</a>
          <a-button type="primary">可领取</a-button>
          <a-button type="primary" @click="openSerialPort" :disabled="isPortOpen">打开串口</a-button>
          <a-button type="primary" @click="closeSerialPort" :disabled="!isPortOpen">关闭串口</a-button>
        </a-space>
      </div>
      <a-table
          size="middle"
          rowKey="id"
          :loading="data.loading"
          :columns="columns"
          :data-source="data.userList"
          :scroll="{ x: 'max-content' }"
          :row-selection="rowSelection"
          :pagination="{
          size: 'default',
          current: data.page,
          pageSize: data.pageSize,
          onChange: (current) => (data.page = current),
          showSizeChanger: false,
          showTotal: (total) => `共${total}条数据`,
        }"
      >
        <template #bodyCell="{ text, record, index, column }">
          <template v-if="column.key === 'operation'">
            <span>
              <a @click="handleEdit(record)">领取</a>

            </span>
          </template>
        </template>
      </a-table>
    </div>

    <!--弹窗区域-->
    <div>
      <!--
      <a-modal
  :visible="itemModal.visible"
  title="物品详情"
  :footer="null"
  @cancel="itemModal.visible = false"
>
  <a-descriptions bordered :column="2">
    <a-descriptions-item label="物品列表">
      {{ itemModal.items }}
    </a-descriptions-item>
    <a-descriptions-item label="状态">
      <span style="color: green;">{{ itemModal.status }}</span>
    </a-descriptions-item>
  </a-descriptions>
</a-modal>
      -->
      <a-modal
  :visible="itemModal.visible"
  title="物品详情"
  :footer="null"
  @cancel="itemModal.visible = false"
>
  <a-descriptions bordered :column="2">
    <template v-for="(status, item) in itemModal.items" :key="item">
      <a-descriptions-item :label="item">
        <span :style="{
          color: status === 1 ? 'green' :
                 status === 0 ? '#ffcc00' :
                 'red'
        }">
          {{ status === 1 ? '未损坏' :
             status === 0 ? '已损坏' :
             '缺失' }}
        </span>
      </a-descriptions-item>
    </template>
  </a-descriptions>
</a-modal>
      <a-modal
          :visible="modal.visile"
          :forceRender="true"
          :title="modal.title"
          ok-text="确认"
          cancel-text="取消"
          @cancel="handleCancel"
          @ok="handleCancel"
      >
        <div>

          <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="modal.form" :rules="modal.rules">
            <a-row :gutter="24">
              <a-col span="24">
                <a-form-item label="编号" name="id">
                  <a-input-number disabled
                    placeholder="请输入编号"
                    v-model:value="modal.form.id"
                    :controls="false"
                    style="width: 100%"
                  />
                </a-form-item>
              </a-col>
                      <a-col span="24">
                  <a-descriptions bordered :column="2">
                    <template v-for="(status, item) in modal.form.item ? JSON.parse(modal.form.item) : {}" :key="item">
                      <a-descriptions-item :label="item">
                        <span :style="{
                          color: status === 1 ? 'green' :
                                 status === 0 ? '#ffcc00' :
                                 'red'
                        }">
                          {{ status === 1 ? '未损坏' :
                             status === 0 ? '已损坏' :
                             '缺失' }}
                        </span>
                      </a-descriptions-item>
                    </template>
                  </a-descriptions>
              </a-col>

              <a-col span="24">
                <a-form-item label="柜号" name="cabinet">
                  <a-input-number disabled
                    placeholder="请输入柜号"
                    v-model:value="modal.form.cabinet"
                    :controls="false"
                    style="width: 100%"
                  />
                </a-form-item>
              </a-col>

            </a-row>
          </a-form>
          <a-button type="primary" @click="opendoor" >开启柜门</a-button>
          <a>&nbsp&nbsp&nbsp&nbsp&nbsp</a>

          <a>&nbsp&nbsp&nbsp&nbsp&nbsp</a>
          <a-button type="primary" @click="lingqu" :disabled="!modal.openflag">领取</a-button>
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script setup lang="ts">
import {FormInstance, message} from 'ant-design-vue';
import {createApi, listApi, updateApi, deleteApi,returnjingjucreateApi} from '/@/api/jingju';

// 添加串口相关状态
const port = ref<SerialPort | null>(null);
const isPortOpen = ref(false);

// 打开串口函数
const openSerialPort = async () => {
  try {
    // 请求用户选择串口
    port.value = await navigator.serial.requestPort();

    // 打开串口
    await port.value.open({
      baudRate: 9600, // 波特率
      dataBits: 8,    // 数据位
      parity: 'none', // 校验位
      stopBits: 1,    // 停止位
      flowControl: 'none' // 流控制
    });

    isPortOpen.value = true;
    message.success('串口已成功打开');
  } catch (error) {
    console.error('打开串口失败:', error);
    message.error('打开串口失败');
  }
};

// 关闭串口函数
const closeSerialPort = async () => {
  if (port.value) {
    try {
      await port.value.close();
      isPortOpen.value = false;
      message.success('串口已关闭');
    } catch (error) {
      console.error('关闭串口失败:', error);
      message.error('关闭串口失败');
    }
  }
};
const lingqu = async () => {
  if (!modal.form.id) {
    message.warning('请选择要领取的项目');
    return;
  }

  try {


    await returnjingjucreateApi({
      jingju: modal.form.id,
      getcabinet: modal.form.cabinet,
      people: 200340019
    });
    message.success('领取成功');
    await updateApi({ id: modal.form.id }, { id: modal.form.id, status: 1 });
    hideModal();
    getDataList(); // Refresh the list after update
  } catch (error) {
    console.error('领取失败:', error);
    message.error('领取失败');

  };


};
const columns = reactive([

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
    title: '物品',
    dataIndex: 'item',
    key: 'item',
    customRender: ({ text }) => {
      return h('a', { type: 'primary', onClick: () => showItemDetail(text) }, '查看');
    }
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



const opendoor = async () => {
  if (!isPortOpen.value) {
    message.warning('请先打开串口');
    return;
  }

  try {
    const writer = port.value?.writable?.getWriter();
    if (writer) {
      // 发送开柜命令（根据你的硬件协议修改）
      const hexString = '8A01021198';
      const hexBytes = new Uint8Array(hexString.length / 2);
      for (let i = 0; i < hexString.length; i += 2) {
        hexBytes[i / 2] = parseInt(hexString.substr(i, 2), 16);
      }
      // Send the binary data
      await writer.write(hexBytes);
      writer.releaseLock();
      message.success('柜门已开启');
      modal.openflag = true;
    }
  } catch (error) {
    console.error('发送命令失败:', error);
    message.error('开启柜门失败');
  }
};


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
  openflag:false,
  visile: false,
  editFlag: false,
  title: '',
  form: {
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
import {useUserStore} from "/@/store";

const userStore = useUserStore();
const getDataList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
    page: data.page,
    pageSize: data.pageSize,
    people: userStore.admin_user_name,
  })
      .then((res) => {
        data.loading = false;
        console.log(res);

        // Filter to show only first occurrence of each type
        const seenTypes = new Set();
        data.userList = res.data
          .filter((item: any) => {
            if (!seenTypes.has(item.type)) {
              seenTypes.add(item.type);
              return true;
            }
            return false;
          })
          .map((item: any) => ({
            id: item.id,
            type: item.type,
            item: JSON.stringify(item.item),
            cabinet: item.cabinet,
            last_people: item.last_people
          }));
      })
      .catch((err) => {
        data.loading = false;
        console.log(err);
        data.userList = [];
        data.page = 1;
        data.pageSize = 10;
        data.selectedRowKeys = [];
        data.keyword = ''
        data.currentAdminUserName = '';
        data.loading = false;
        //message.error("您有未归还的警具或您暂无权领取警具");
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
  modal.openflag= false;
  modal.title = '新增';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
};
const handleEdit = (record: any) => {
  resetModal();
  modal.visile = true;
  modal.editFlag = true;
  modal.title = '领取';
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
  modal.openflag = false;
};
</script>

<style scoped lang="less">
.page-view {
  min-height: 100%;
  background: #fff;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.table-operations {
  margin-bottom: 16px;
  text-align: left;
}

.table-operations > button {
  margin-right: 8px;
}
</style>
