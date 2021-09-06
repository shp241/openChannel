<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 数据表单
                </el-breadcrumb-item>
                <el-breadcrumb-item>数据上传</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <el-form ref="formRef" :rules="rules" :model="form" label-width="80px">
                    <el-form-item label="上传人员" prop="name">
                        <el-input v-model="form.name"></el-input>
                    </el-form-item>
                    <el-form-item label="位置" prop="region">
                        <el-select v-model="form.region" placeholder="请选择">
                            <el-option key="n1" label="测流槽1" value="n1"></el-option>
                            <el-option key="n2" label="测流槽2" value="n2"></el-option>
                            <el-option key="n3" label="测流槽3" value="n3"></el-option>
                            <el-option key="n4" label="测流槽4" value="n4"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="日期时间">
                        <el-col :span="11">
                            <el-form-item prop="date1">
                                <el-date-picker type="date" placeholder="拍摄日期" v-model="form.date1"
                                    style="width: 100%;"></el-date-picker>
                            </el-form-item>
                        </el-col>
                        <el-col class="line" :span="2">-</el-col>
                        <el-col :span="11">
                            <el-form-item prop="date2">
                                <el-time-picker placeholder="拍摄时间" v-model="form.date2" style="width: 100%;">
                                </el-time-picker>
                            </el-form-item>
                        </el-col>
                    </el-form-item>
                     <el-form-item label="视频截取">
                        <el-col :span="11">
                            <el-form-item prop="date3">
                                <el-time-picker placeholder="开始时间:时-分-秒" v-model="form.date3" style="width: 100%;">
                                </el-time-picker>
                            </el-form-item>
                        </el-col>
                        <el-col class="line" :span="2">-</el-col>
                        <el-col :span="11">
                            <el-form-item prop="date4">
                                <el-time-picker placeholder="结束时间:时-分-秒" v-model="form.date4" style="width: 100%;">
                                </el-time-picker>
                            </el-form-item>
                        </el-col>
                    </el-form-item>
                    <el-form-item label="地区" prop="options">
                        <el-cascader :options="options" v-model="form.options"></el-cascader>
                    </el-form-item>


                    <el-form-item label="附加备注" prop="desc">
                        <el-input type="textarea" rows="5" v-model="form.desc"></el-input>
                    </el-form-item>
                    
                    <el-card
                        header="ele-form-image-uploader 演示"
                        shadow="never"
                        style="max-width: 1250px;margin: 20px auto;"
                        >
                    <ele-form
                        :form-data="formData"
                        :form-desc="formDesc"
                        :request-fn="handleRequest"
                        @request-success="handleSuccess"
                        />
                    </el-card>


                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">表单提交</el-button>
                        <el-button @click="onReset">重置表单</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>



<script>
import { reactive, ref } from "vue";
import { ElMessage } from "element-plus";
//import EleForm from 'vue-ele-form';
//import EleFormVideoUploader from 'vue-ele-form-video-uploader';
// 注册 ele-form
export default {
    name: "baseform",
    setup() {
        const options = [
            {
                value: "bupt",
                label: "北京邮电大学",
                children: [
                    {
                        value: "east",
                        label: "东部",
                        children: [
                            {
                                value: "gym",
                                label: "体育馆测流槽",
                            },
                            {
                                value: "playground",
                                label: "操场测流槽",
                            },
                        ],
                    },
                    {
                        value: "west",
                        label: "西部",
                        children: [
                            {
                                value: "dormitory1",
                                label: "学一测流槽1",
                            },
                            {
                                value: "dormitory2",
                                label: "学二测流槽1",
                            },
                        ],
                    },
                                        {
                        value: "south",
                        label: "南部",
                        children: [
                            {
                                value: "classroom1",
                                label: "教三测流槽",
                            },
                            {
                                value: "classroom2",
                                label: "教二测流槽",
                            },
                        ],
                    },
                                        {
                        value: "north",
                        label: "北部",
                        children: [
                            {
                                value: "basement1",
                                label: "创新基地测流槽",
                            },
                        ],
                    },
                ],
            },
        ];
        const rules = {
            name: [
                { required: true, message: "请输入表单名称", trigger: "blur" },
            ],
        };
        const formRef = ref(null);
        const form = reactive({
            name: "",
            region: "",
            date1: "",
            date2: "",
            delivery: true,
            type: ["测流槽位置"],
            resource: "测流槽1",
            desc: "",
            options: [],
        });
        // 提交
        const onSubmit = () => {
            // 表单校验
            formRef.value.validate((valid) => {
                if (valid) {
                    console.log(form);
                    ElMessage.success("提交成功！");
                } else {
                    return false;
                }
            });
        };
        // 重置
        const onReset = () => {
            formRef.value.resetFields();
        };

        return {
            options,
            rules,
            formRef,
            form,
            onSubmit,
            onReset,
            
        };
    },

    data () {
    return {
      formData: {},
      formDesc: {
        video: {
          label: '团队介绍',
          type: 'video-uploader',
          attrs: {
            fileSize: 20,
            action: 'https://jsonplaceholder.typicode.com/posts',
            responseFn (response, file) {
              return URL.createObjectURL(file.raw)
            }
          }
        }
      }
    }
  },
  methods: {
    handleRequest (data) {
      console.log(data)
      return Promise.resolve()
    },
    handleSuccess () {
      this.$message.success('提交成功')
    }
  },
  mounted () {}
};
</script>