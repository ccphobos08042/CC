<template>
  <div id="userLayout">
    <div class="user-layout-header">
      <img class="logo" :src="logoImage" alt="">
      <span>警具管理系统</span>
    </div>
    <div class="main-container">
      <div class="main">
        <div class="main_right">
          <h2 class="sys_title">{{ flag?"管理员":"安全员" }}登录&nbsp;<a-button type="primary" @click="toggleLoginType">前往{{flag?"安全员登录":"管理员登录"}}</a-button>
          </h2>
          <a-form
              ref="myform"
              layout="vertical"
              :model="data.loginForm"
              :rules="data.rules"
              :hideRequiredMark="true"
          >
            <a-form-item  v-if="flag" name="username" label="账号" :colon="false">
              <a-input
                  size="large"
                  placeholder="请输入登录账号"
                  v-model:value="data.loginForm.username"
                  @pressEnter="handleSubmit">
              </a-input>
            </a-form-item>
            <a-form-item  v-if="flag" name="password" label="密码" :colon="false">
              <a-input
                  size="large"
                  type="password"
                  placeholder="请输入登录密码"
                  v-model:value="data.loginForm.password"
                  @pressEnter="handleSubmit">
              </a-input>
            </a-form-item>
            <a-form-item  v-if="!flag" name="jobNumber" label="工号" :colon="false">
                <a-input
                  size="large"
                  placeholder="请输入工号"
                  v-model:value="data.loginForm.jobNumber"
                  @pressEnter="handleSubmit"
                />
              </a-form-item >
              <a-form-item  v-if="!flag" label="人脸识别" :colon="false">
                <a-button
                  size="large"
                  block

                  @click="handleFaceRecognition"
                >
                  点击拍照
                </a-button>
                <img
    v-if="data.capturedImage"
    :src="data.capturedImage"
    class="preview-image"
    alt="拍摄预览"
  />
              </a-form-item>
            <a-form-item style="padding-top: 24px">
              <a-button
                  class="login-button"
                  type="primary"
                  :loading="loginBtn"
                  size="large"
                  block
                  @click="handleSubmit"
              >
                登录
              </a-button>
            </a-form-item>
          </a-form>

          <div class="error-tip"></div>
        </div>
      </div>

    </div>
    <footer class="footer">
      <div class="copyright">
        <span></span>
      </div>
    </footer>
  </div>

</template>

<script setup lang="ts">
import {useUserStore} from '/@/store';
import logoImage from '/@/assets/images/k-logo.png';

const router = useRouter();
const userStore = useUserStore();

import {message} from "ant-design-vue";

const myform = ref()
const flag = ref(true) // 改为响应式引用

// 添加切换方法

const loginBtn = ref<Boolean>(false)
const checked = ref<Boolean>(false)
const data = reactive({
  loginForm: {
    username: '',
    password: '',
    jobNumber: ''
  },
  rules: {
    username: [
      { required: true, message: '请输入用户名', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' }
    ],
    jobNumber: [ // 新增工号校验
      { required: true, message: '请输入工号', trigger: 'blur' }
    ]
  },
  capturedImage: null as string | null
})
const toggleLoginType = () => {
  flag.value = !flag.value
}
const handleSubmit = () => {
  myform.value?.validate().then(() => {
    if (!flag.value && !data.capturedImage) { // 安全员模式必须拍摄照片
      message.warn('请先进行人脸识别')
      return
    }
    handleLogin()
  }).catch(() => {
    message.warn('表单填写不完整')
  })
}
const handleFaceRecognition = async () => {
  try {
    // 请求摄像头权限
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(device => device.kind === 'videoinput');

    if (videoDevices.length === 0) {
      throw new Error('没有找到摄像头设备');
    }

    // 如果有多个摄像头，让用户选择
    let deviceId;
    if (videoDevices.length > 1) {

      const selected = confirm(`检测到 ${videoDevices.length} 个摄像头，是否使用1号摄像头\n`);
      deviceId = selected ? videoDevices[0].deviceId : videoDevices[1].deviceId;
    } else {
      deviceId = videoDevices[0].deviceId;
    }

    const stream = await navigator.mediaDevices.getUserMedia({
      video: true
    });
    const video = document.createElement('video');
    video.srcObject = stream;
    await video.play();

    // 创建拍照用的canvas
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
    data.capturedImage = lastPhoto;

    // 关闭摄像头流
    stream.getTracks().forEach(track => track.stop());
  } catch (error) {
    message.error('摄像头访问失败: ' + (error as Error).message);
  }
}
const handleLogin = () => {
  const loginData = flag.value
    ? {
        username: data.loginForm.username,
        password: data.loginForm.password
      }
    : {
        username: data.loginForm.jobNumber,
        password: data.capturedImage // 使用拍摄的图片作为密码
      };

  userStore.adminLogin(loginData)
    .then(res => {
      loginSuccess()
    }).catch(err => {
      message.warn(err.msg || '登录失败')
    })
}

const loginSuccess = () => {
  router.push({ path: '/admin' })
  message.success('登录成功！')
}


</script>

<style lang="less" scoped>
.preview-image {
  display: block;
  margin-top: 16px;
  max-width: 100%;
  max-height: 200px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
#userLayout {
  position: relative;
  height: 100vh;

  .user-layout-header {
    height: 80px;
    padding: 0 24px;
    color: fade(#000, 85%);
    font-size: 24px;
    font-weight: bold;
    line-height: 80px;

    .logo {
      width: 36px;
      height: 36px;
      margin-right: 16px;
      margin-top: -4px;
    }
  }

  .main-container {
    width: 100%;
    height: calc(100vh - 160px);
    background-image: url('../images/admin-login-bg.jpg');
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;

    .main {
      position: absolute;
      right: 80px;
      top: 50%;
      display: flex;
      transform: translate(0, -50%);
      border-radius: 8px;
      overflow: hidden;
      -webkit-box-shadow: 2px 2px 6px #aaa;
      box-shadow: 2px 2px 6px #aaa;

      .main_right {
        background: #ffffff;
        padding: 24px;
        width: 420px;
        user-select: none;

        .sys_title {
          font-size: 24px;
          color: fade(#000, 85%);
          font-weight: bold;
          user-select: none;
          padding-bottom: 8px;
        }

        :deep(.ant-form-item label) {
          font-weight: bold;
        }

        .flex {
          align-items: center;
          display: flex;
          justify-content: space-between;
        }

        .forget_password {
          cursor: pointer;
        }

        .login-button {
          background: linear-gradient(128deg, #00aaeb, #00c1cd 59%, #0ac2b0 100%);
        }
      }

      .error-tip {
        text-align: center;
      }
    }
  }

  .footer {
    height: 80px;
  }
}

</style>
