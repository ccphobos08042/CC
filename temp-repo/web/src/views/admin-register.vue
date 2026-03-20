<template>
  <div id="userLayout">
    <div class="user-layout-header">
      <img class="logo" :src="logoImage" alt="">
      <span>警具管理系统</span>
    </div>
    <div class="main-container">
      <div class="main">
        <div class="main_right">
          <h2 class="sys_title">管理员注册</h2>
          <a-form
              ref="myform"
              layout="vertical"
              :model="data.loginForm"
              :rules="data.rules"
              :hideRequiredMark="true"
          >
            <a-form-item name="username" label="账号" :colon="false">
              <a-input
                  size="large"
                  placeholder="请输入登录账号"
                  v-model:value="data.loginForm.username"
                  @pressEnter="handleSubmit">
              </a-input>
            </a-form-item>
            <a-form-item name="password" label="密码" :colon="false">
              <a-input
                  size="large"
                  type="password"
                  placeholder="请输入登录密码"
                  v-model:value="data.loginForm.password"
                  @pressEnter="handleSubmit">
              </a-input>
            </a-form-item>
            <a-form-item name="repassword" label="确认密码" :colon="false">
              <a-input
                  size="large"
                  type="password"
                  placeholder="请再次输入登录密码"
                  v-model:value="data.loginForm.repassword"
                  @pressEnter="handleSubmit">
              </a-input>
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
                注册
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
import {registerApi} from '/@/api/user';
import logoImage from '/@/assets/images/k-logo.png';

const router = useRouter();
const userStore = useUserStore();

import {message} from "ant-design-vue";

const myform = ref()

const loginBtn = ref<Boolean>(false)
const checked = ref<Boolean>(false)
const data = reactive({
  loginForm: {
    username: '',
    password: '',
    repassword: '',
    status: '0',
    role: '1'
  },
  rules: {
    username: [
      {required: true, message: '请输入用户名', trigger: 'blur'}
    ],
    password: [
      {required: true, message: '请输入密码', trigger: 'blur'}
    ],
    repassword: [
      {required: true, message: '请输入确认密码', trigger: 'blur'}
    ]
  }
})

const handleSubmit = () => {
  myform.value?.validate().then(() => {
    handleRegister()
  }).catch(() => {
    message.warn('不能为空')
  })
}

const handleRegister = () => {
  if(data.loginForm.password !== data.loginForm.repassword){
    message.warn('两次密码不一致')
    return;
  }
  registerApi({
    username: data.loginForm.username,
    password: data.loginForm.password,
    status: data.loginForm.status,
    role: data.loginForm.role
  })
      .then((res) => {
        router.push({ path: '/admin' })
       message.success('注册成功！')
      })
      .catch((err) => {
        console.log(err);
        message.warn(err.msg || "注册失败")
      });

}

const loginSuccess = () => {
  router.push({path: '/admin'})
  message.success('注册成功！')
}


</script>

<style lang="less" scoped>

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
