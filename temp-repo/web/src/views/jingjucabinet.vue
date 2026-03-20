<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>


          <a-button type="primary" @click="openSerialPort" :disabled="isPortOpen">打开串口</a-button>
          <a-button type="primary" @click="closeSerialPort" :disabled="!isPortOpen">关闭串口</a-button>

          <a-button type="primary" @click="handleAdd">新增</a-button>
          <a-button @click="handleBatchDelete">批量删除</a-button>
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
              <a @click="handleEdit(record)">编辑</a>
              <a-divider type="vertical"/>
              <a-popconfirm title="确定删除?" ok-text="是" cancel-text="否" @confirm="confirmDelete(record)">
                <a href="#">删除</a>
              </a-popconfirm>
              <a-divider type="vertical"/>
              <a-popconfirm title="确定开启柜门?" ok-text="是" cancel-text="否" @confirm="opendoor(record)">
                <a href="#">开启</a>
              </a-popconfirm>
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
                 'red'}"
              >
                {{ status === 1 ? '未损坏' :
                  status === 0 ? '已损坏' : '缺失' }}
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
          @ok="handleOk"
      >
        <div>

          <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="modal.form" :rules="modal.rules">
            <a-row :gutter="24">
              <a-col span="24">
                <a-form-item label="编号" name="id">
                  <a-input-number
                    placeholder="请输入编号"
                    v-model:value="modal.form.id"
                    :controls="false"
                    style="width: 100%"
                  />
                </a-form-item>
              </a-col>


              <a-col span="24">
                <a-form-item label="类型" name="status">
                  <a-select
                    placeholder="请选择类型"
                    v-model:value="modal.form.type"
                    style="width: 100%"
                  >
                    <a-select-option :value="1">警具柜</a-select-option>
                    <a-select-option :value="2">充电柜</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>


              <a-col span="24">
                <a-form-item label="容量" name="cabinet">
                  <a-input-number
                    placeholder="请输入容量"
                    v-model:value="modal.form.capacity"
                    :controls="false"
                    style="width: 100%"
                  />
                </a-form-item>
              </a-col>

              <a-col span="24">
                <a-form-item label="位置" name="last_people">
                  <a-select
                    placeholder="请选择城市"
                    v-model:value="selectedCity"
                    style="margin-bottom: 16px"
                    @change="handleCityChange"
                  >
                    <a-select-option v-for="city in cities" :key="city" :value="city">
                      {{ city }}
                    </a-select-option>
                  </a-select>
                  <a-select
                    placeholder="请选择机场"
                    v-model:value="selectedAirport"
                    :disabled="!selectedCity"
                    style="margin-bottom: 16px"
                  >
                    <a-select-option v-for="airport in airports" :key="airport" :value="airport">
                      {{ airport }}
                    </a-select-option>
                  </a-select>
                  <a-input
                    placeholder="请输入具体位置"
                    v-model:value="inputLocation"
                    allowClear
                  />
                </a-form-item>
              </a-col>



            </a-row>
          </a-form>
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script setup lang="ts">
import {FormInstance, message} from 'ant-design-vue';
import {createApi, listApi, updateApi, deleteApi} from '/@/api/jingjucabinet';


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
          typeText = '大警具包柜';
          break;
        case 0:
          typeText = '小警具包柜';
          break;
        default:
          typeText = '充电柜';
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
          statusText = '正常';
          color = '#00ff00';
          break;
        case 2:
          statusText = '容量不足';
          color = '#ff9500';
          break;
        case 0:
          statusText = '数量不足';
          color = '#ff0000';
          break;
        default:
          statusText = '未启用';
          color = '#8c8c8c';
      }
      return h('span', { style: { color } }, statusText);
    }
  },
  {
    title: '容量',
    dataIndex: 'capacity',
    key: 'capacity',
  },
  {
    title: '当前数量',
    dataIndex: 'quantity',
    key: 'quantity',
  },
  {
    title: '位置',
    dataIndex: 'location',
    key: 'location',
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
// ... existing code ...
const cities = ref(['北京', '上海', '广州', '深圳', '成都','天津','西安','武汉','南京','杭州','重庆','长沙','合肥']); // 示例城市列表
const airports = ref<string[]>([]);

// 城市-机场映射数据
const cityAirportMap = {
  北京: ['北京首都国际机场', '北京大兴国际机场'],
  上海: ['上海浦东国际机场', '上海虹桥国际机场'],
  广州: ['广州白云国际机场'],
  深圳: ['深圳宝安国际机场'],
  成都: ['成都双流国际机场', '成都天府国际机场'],
  天津: ['天津滨海国际机场'],
  西安: ['西安咸阳国际机场'],
  武汉: ['武汉天河国际机场'],
  南京: ['南京禄口国际机场'],
  杭州: ['杭州萧山国际机场'],
  重庆: ['重庆江北国际机场'],
  长沙: ['长沙黄花国际机场'],
  合肥: ['合肥新桥国际机场'],
};



// 在modal.form中添加city字段
const modal = reactive({
  openflag: false,
  visile: false,
  editFlag: false,
  title: '',
  form: {
    id: undefined,
    type: undefined,
    status: undefined,
    capacity: undefined,
    quantity: undefined,
    location: undefined,
  },
});
// ... existing code ...

const itemModal = reactive({
  visible: false,
  items: {} as Record<string, number>
});
const myform = ref<FormInstance>();

onMounted(() => {
  getDataList();
});
const port = ref<SerialPort | null>(null);
const isPortOpen = ref(false);
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
const opendoor = async (record) => {

  if (!isPortOpen.value) {

    message.warning('请先打开串口');
    return;
  }

  try {
    const writer = port.value?.writable?.getWriter();
    if (writer) {
      const guihao = record.id;
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

      getDataList();
      modal.openflag = true;
    }
  } catch (error) {
    console.error('发送命令失败:', error);
    message.error('开启柜门失败');
  }
};
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
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
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
const selectedCity = ref(''); // 选择的城市
const selectedAirport = ref(''); // 选择的机场
const inputLocation = ref(''); // 输入的具体位置

const handleCityChange = (city: string) => {
  selectedCity.value = city;
  selectedAirport.value = ''; // 清空机场选择
  inputLocation.value = ''; // 清空输入内容
  airports.value = cityAirportMap[city] || [];
};
const handleOk = () => {
  myform.value
      ?.validate()
      .then(() => {
        // 拼接城市、机场和输入内容作为location
        if (selectedCity.value && selectedAirport.value) {
          modal.form.location = `${selectedCity.value} - ${selectedAirport.value}`;
          if (inputLocation.value) {
            modal.form.location += ` - ${inputLocation.value}`;
          }
        }

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
