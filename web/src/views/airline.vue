<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-button @click="handleImport">导入</a-button>
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
            </span>
          </template>
        </template>
      </a-table>
    </div>

    <!--弹窗区域-->
    <div>
<a-modal
  :visible="itemModal.visible"
  title="安全员详情"
  :footer="null"
  @cancel="itemModal.visible = false"
>
  <a-table
    :data-source="itemModal.items"
    :columns="[

      { title: '安全员ID', dataIndex: 'value' }
    ]"
    bordered
    size="small"
    :pagination="false"
  />
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
          <a-form-item label="出发时间" name="begin_time">
            <a-input
              placeholder="请输入出发时间"
              v-model:value="modal.form.begin_time"
            />
          </a-form-item>
        </a-col>
        <a-col span="24">
          <a-form-item label="到达时间" name="end_time">
            <a-input
              placeholder="请输入到达时间"
              v-model:value="modal.form.end_time"
            />
          </a-form-item>
        </a-col>
        <a-col span="24">
          <a-form-item label="出发机场" name="begin_ariport">
            <a-input
              placeholder="请输入出发机场"
              v-model:value="modal.form.begin_ariport"
            />
          </a-form-item>
        </a-col>
        <a-col span="24">
          <a-form-item label="到达机场" name="end_ariport">
            <a-input
              placeholder="请输入到达机场"
              v-model:value="modal.form.end_ariport"
            />
          </a-form-item>
        </a-col>
        <a-col span="24">
          <a-form-item label="安全员信息" name="people">
            <a-textarea
              placeholder="安全员信息"
              v-model:value="modal.form.people"
              :auto-size="{ minRows: 2, maxRows: 5 }"
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
import {createApi, listApi, updateApi, deleteApi,importApi} from '/@/api/airline';

const columns = reactive([
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
  },
  {
    title: '出发时间',
    dataIndex: 'begin_time',
    key: 'begin_time',
  },
  {
    title: '到达时间',
    dataIndex: 'end_time',
    key: 'end_time',
  },
  {
    title: '出发机场',
    dataIndex: 'begin_ariport',
    key: 'begin_ariport',
  },
  {
    title: '到达机场',
    dataIndex: 'end_ariport',
    key: 'end_ariport',
  },
  {
    title: '安全员信息',
    dataIndex: 'people',
    key: 'people',
    customRender: ({ text }) => {
      return h('a', { type: 'primary', onClick: () => showPeopleDetail(text) }, '查看');
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

const handleImport = () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.xlsx,.csv,xls'; // 根据实际需求调整文件类型
  input.onchange = async (e) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) {
      try {
        const formData = new FormData();
        formData.append('file', file);
        const result=await importApi(formData);
        message.success(result.msg);
        getDataList();
      } catch (error) {
        message.error('导入失败: ' + error.message);
      }
    }
  };
  input.click();
};

const getRandomItems = () => {
  const items = ['警棍', '手铐',  '手套',  '强光手电' ,"催泪喷射器","匕首"];
  const allItems = {};
  items.forEach(item => {
    allItems[item] = 1;
  });
  return JSON.stringify(allItems);
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
const itemModal = reactive({
  visible: false,
  items: [] as Array<{ key: string, value: string }>
});
// 弹窗数据源
const modal = reactive({
  visile: false,
  editFlag: false,
  title: '',
  form: {
    id: undefined,
    begin_time: undefined,
    end_time: undefined,
    begin_ariport: undefined,
    end_ariport: undefined,
    people: undefined,
  },
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
const showPeopleDetail = (text: string) => {
  try {
    const parsed = typeof text === 'string' ? JSON.parse(text) : text;
    itemModal.items = Object.entries(parsed).map(([key, value]) => ({
      key,
      value: String(value)
    }));
    itemModal.visible = true;
  } catch (e) {
    message.error('人员信息格式错误');
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
