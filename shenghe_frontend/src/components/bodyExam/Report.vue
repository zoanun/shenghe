<template>
  <el-dialog :visible.sync="dialogVisible"
             :close-on-click-modal="false"
             :close-on-press-escape="false"
             title="体测报告"
             append-to-body
             width="800px"
             @opened="onOpened"
             @close="onClose"
  >
    <div>
      <div id="printMe">
        <div class="user">
          <el-form v-if="reportData && reportData.current_test && reportData.current_test.length > 0"
                   :inline="true"
          >
            <el-form-item label="用户">
              {{ name }}
            </el-form-item>
            <el-form-item label="年龄">
              {{ age }}
            </el-form-item>
            <el-form-item label="性别">
              {{ sex }}
            </el-form-item>
          </el-form>
        </div>
        <div class="chart">
        </div>
      </div>
      <div slot="footer">
        <el-button v-print="printProp"
                   type="primary"
        >
          打 印
        </el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>
  import request from '@/utils/request.js';
  export default {
    name: 'BodyReport',
    components: {},
    props: {
      reportVisible: {
        type: Boolean,
        default: false
      },
      name: {
        type: String,
        default: ''
      },
      sex: {
        type: String,
        default: ''
      },
      age: {
        type: Number,
        default: 0
      },
      memberId: {
        type: String,
        default: ''
      },
      id: {
        type: Number,
        default: 0
      }
    },
    data () {
      return {
        dialogVisible: false,
        reportData: {},
        contextPath: localStorage.getItem('backendContextPath'),
        printProp: {
          id: 'printMe',
          popTitle: '盛和国际跆拳道'
        }
      };
    },
    watch: {
      reportVisible (val) {
        this.dialogVisible = val;
      }
    },
    methods: {
      onOpened () {
        request({
          url: this.contextPath + '/bc/report',
          method: 'post',
          data: {
            id: this.id,
            memberId: this.memberId
          }
        }).then(result => {
          console.log(result);
          this.reportData = result;
        });
      },
      onClose () {
        this.$emit('update:reportVisible', false);
      },

    }
  };
</script>

<style scoped>
#printMe {
    width: 756px;
    height: 1086px;
    background-image: url(../../assets/img/report-bg.png);
    -webkit-print-color-adjust: exact;
}

@page {
    size: auto; /* auto is the initial value */
    margin: 3mm; /* this affects the margin in the printer settings */
}
html {
    background-color: #ffffff;
    margin: 0px; /* this affects the margin on the html before sending to printer */
}
body {
    border: solid 1px blue;
    margin: 10mm 15mm 10mm 15mm; /* margin you want for the content */
}
</style>

