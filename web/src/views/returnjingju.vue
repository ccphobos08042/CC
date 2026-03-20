<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">

        <a-space>

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
              <a @click="handleEdit(record)">归还</a>

            </span>
          </template>
        </template>
      </a-table>
    </div>

    <!--弹窗区域-->
    <div>


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
                <a-form-item label="编号" name="jingju">

                  <a-input-number disabled
                      v-model:value="modal.form.jingju"
                      :controls="false"
                      placeholder="请输入编号"
                      style="width: 100%"
                  />
                </a-form-item>
              </a-col>

              <a-col span="24">
                  <a-form-item label="归还柜号" name="returncabinet">
                      <a-input-number
                      v-model:value="modal.form.returncabinet"
                      :controls="false"
                      placeholder="请输入编号"
                      style="width: 100%"
                  />
                         </a-form-item>
              </a-col>
              <a-button type="primary" @click="opendoor" >开启柜门</a-button>

            </a-row>
          </a-form>
          <a-button type="primary" @click="yolov8" v-if="!modal.editFlag">检测</a-button>
        </div>
      </a-modal>

    </div>
  </div>
</template>

<script setup lang="ts">
import {FormInstance, message} from 'ant-design-vue';
import {createApi, listApi, updateApi, deleteApi} from '/@/api/returnjingju';
import {updateApi as jjupdate} from '/@/api/jingju';

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
  if (!modal.form.jingju) {
    message.warning('请选择要领取的项目');
    return;
  }

  try {
    await updateApi({ jingju: modal.form.jingju }, { status: 1 });
    message.success('领取成功');
    hideModal();
    getDataList(); // Refresh the list after update
  } catch (error) {
    console.error('领取失败:', error);
    message.error('领取失败');
  }
};
const columns = reactive([
{
    title: 'ID',
    dataIndex: 'id',
    key: 'id',

  },
  {
    title: '包号',
    dataIndex: 'jingju',
    key: 'jingju',

  },
  {
    title: '取出时间',
    dataIndex: 'gettime',
    key: 'gettime',

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
    const guihao=modal.form.returncabinet;

        if (writer) {
      const prefix = '8A01';
      const cabinetNo = guihao.toString().padStart(2, '0');
      const middle = '11';

      // 计算异或校验和
      let xorChecksum = 0;
      const bytes = [
        parseInt(prefix.substr(0,2), 16),
        parseInt(prefix.substr(2,2), 16),
        parseInt(cabinetNo, 16),
        parseInt(middle, 16)
      ];

      bytes.forEach(byte => {
        xorChecksum ^= byte; // 逐字节异或
      });

      const checksum = xorChecksum.toString(16).padStart(2, '0').toUpperCase();

      const hexString = prefix + cabinetNo + middle + checksum;
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
    jingju: undefined,
    returncabinet: undefined,
    item: undefined,
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

        // 移除类型过滤逻辑，直接显示所有数据
        data.userList = res.data.map((item: any) => ({
          id: item.id,
          jingju: item.jingju,
          gettime: item.gettime,
        }));
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
  modal.openflag= false;
  modal.title = '新增';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
};
const handleEdit =async (record: any) => {
  resetModal();
  modal.visile = true;
  modal.editFlag = true;
  modal.title = '归还';

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
  deleteApi({jingjus: record.jingju})
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
                jjupdate({ id: modal.form.jingju }, {id:modal.form.jingju, status: 2,cabinet: modal.form.returncabinet});

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
