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
            <span v-if="record.zhuangtai==0">
              <a-popconfirm title="确定开锁取出?" ok-text="是" cancel-text="否" @confirm="opendoor(record,1)">
                <a href="#">取出</a>
              </a-popconfirm>
            </span>
            <span v-if="record.zhuangtai==1">
              <a-popconfirm title="确定开锁放回?" ok-text="是" cancel-text="否" @confirm="opendoor(record,2)">
                <a href="#">放回</a>
              </a-popconfirm>
            </span>
          </template>
        </template>

      </a-table>
    </div>

    <!--弹窗区域-->

  </div>
</template>

<script setup lang="ts">
import {FormInstance, message} from 'ant-design-vue';
import {createApi, listApi, updateApi, deleteApi,jjupdateApi,jjlistApi} from '/@/api/baoxiu';


const columns = reactive([
  {
    title: 'ID',
    dataIndex: 'bianhao',
    key: 'bianhao',
  },
  {
    title: '物品',
    dataIndex: 'wupin',
    key: 'wupin',
  },
  {
    title: '柜号',
    dataIndex: 'guanhao',
    key: 'guanhao',
  },
  {
    title: '包号',
    dataIndex: 'baohao',
    key: 'baohao',
  },
  {
    title: '报修时间',
    dataIndex: 'baoxiushijian',
    key: 'baoxiushijian',
  },
  {
    title: '报修人',
    dataIndex: 'baoxiuren',
    key: 'baoxiuren',

  },
    {
  title: '状态',
  dataIndex: 'zhuangtai',
  key: 'zhuangtai',
  customRender: ({ text }) => {
    let statusText = '';
    let color = '';
    switch (text) {
      case 0:
        statusText = '待修理';
        color = 'red'; // 红色
        break;
      case 1:
        statusText = '修理中';
        color = 'orange'; // 橙色
        break;
      case 2:
        statusText = '修理完成';
        color = 'green'; // 绿色
        break;
      default:
        statusText = '未知状态';
        color = 'gray'; // 灰色
    }
    return h('span', { style: { color } }, statusText);
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
  form: {
    bianhao: undefined,
    wupin: undefined,
    guanhao: undefined,
    baohao: undefined,
    baoxiushijian: undefined,
    baoxiuren: undefined,
    zhuangtai: undefined
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



const confirmDelete = (record: any) => {
  console.log('delete', record);
  deleteApi({ids: record.bianhao})
      .then((res) => {
        getDataList();
      })
      .catch((err) => {
        message.error(err.msg || '删除失败');
      });
};


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

// ... existing code ...

const opendoor = async (record,status) => {

  if (!isPortOpen.value) {

    message.warning('请先打开串口');
    return;
  }

  try {
    const writer = port.value?.writable?.getWriter();
    if (writer) {
      const guihao = record.guanhao;
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
      await updateApi({ id: record.bianhao }, { zhuangtai: status });
      if (record.zhuangtai === 1) {
        const jjListRes = await jjlistApi({ id: record.baohao });
        const currentItem = { ...jjListRes.data.item };

        // 修改 wupin 字段
        currentItem[record.wupin] = 1;

        // 调用 jjupdateApi 修改 item
        const jjRes = await jjupdateApi({ id:record.baohao }, {
          id:record.baohao,
          item: currentItem
        });
        const allItemsOne = Object.values(jjRes.data.item).every(val => val === 1);
        if (allItemsOne) {
          await jjupdateApi({ id: record.baohao }, {id: record.baohao, status: 2 });
        }
      }
      getDataList();
      modal.openflag = true;
    }
  } catch (error) {
    console.error('发送命令失败:', error);
    message.error('开启柜门失败');
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
  text-align: right;
}

.table-operations > button {
  margin-right: 8px;
}
</style>
