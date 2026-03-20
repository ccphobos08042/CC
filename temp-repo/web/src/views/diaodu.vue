<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-button type="primary" @click="handleAdd">新增</a-button>

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
          <a-form-item label="拍照">
            <a-button @click="handleTakePhoto" type="primary">拍照</a-button>
            <img v-if="modal.form.img" :src="modal.form.img" style="display: block; max-width: 200px; margin-top: 10px;"/>
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
import axios from "axios";import {createApi,listApi,deleteApi} from '/@/api/diaodu';


const columns = reactive([
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
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
    img: undefined,
  },
});

const myform = ref<FormInstance>();

onMounted(() => {
  getDataList();
});
const handleTakePhoto = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    const video = document.createElement('video');
    video.srcObject = stream;
    await video.play();

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
const takePhoto = () => {
      ctx?.drawImage(video, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL('image/jpeg');
    };

    // 连拍20张照片
    let lastPhoto = '';
    for (let i = 0; i < 20; i++) {
      lastPhoto = takePhoto();
      await new Promise(resolve => setTimeout(resolve, 100)); // 每张照片间隔100ms
    }

    // 使用最后一张照片
    
    const photo = lastPhoto;
    stream.getTracks().forEach(track => track.stop());
    modal.form.img = photo;

  } catch (error) {
    console.error('摄像头访问失败:', error);
    message.error('摄像头访问失败: ' + error.message);
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
        // 处理嵌套的 user_id_list 数据
        data.userList = res.data.user_id_list.map((userId: string) => {
          return { id: userId };  // 将字符串转换为对象格式
        });
      })
      .catch((err) => {
        // ... 错误处理保持不变 ...
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




// ... 现有代码 ...
const handleOk = () => {
  myform.value?.validate().then(() => {
    // 构建提交数据
    const formData = {
      id: modal.form.id,
      img: modal.form.img
    };

    createApi(formData)
      .then(res => {
        message.success('操作成功');
        getDataList(); // 刷新列表
        hideModal();   // 关闭弹窗
      })
      .catch(err => {
        message.error(err.msg || '提交失败');
      });
  }).catch(error => {
    console.log('验证失败:', error);
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
