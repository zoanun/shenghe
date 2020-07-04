<template>
  <el-dialog :visible.sync="dialogVisible"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    title="体测报告"
    append-to-body
    width="800px"
    @opened="onOpened"
    @close="onClose">
    <div>
      <div id="printMe">
        <div class='user'>
          <el-form :inline="true"
            v-if="reportData && reportData.length > 0">
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
        <div class='chart'>
          <div class='line'
            v-for="item in reportData"
            :key="item.id">

            <span class="item-title">
              项目： {{ item.name }} ( 国标值： {{ item.standardValue }}, 测量值： {{ item.score }})
            </span>
            <br />

            <div v-for="(level, idx) in item.level"
              :key="level.periodType + 'score'">
              <span v-if="idx!==0"
                class="score">{{ level.lowScore}}</span>
            </div><br />

            <div v-for="(level) in item.level"
              class='tag'
              :key="level.periodType + 'tag'">
              <span v-if="level.inLevel === 'Y'"
                :style="{left: (item.score - level.lowScore) / (level.highScore - level.lowScore) * 100 - 5 + 'px'}"><img src="@/assets/img/tag.png"></span>
            </div>
            <br />

            <div v-for="level in item.level"
              class='bar'
              :style="{'background-color': level.color}"
              :key="level.periodType + 'bar'">
            </div><br />

            <div v-for="(level) in item.level"
              class='name'
              :key="level.periodType + 'name'">
              <span>{{ level.periodName }}</span>
            </div>
            <br />
            <br />
            <span v-for="(level) in item.level"
              class='desc'
              :key="level.periodType + 'scoreDesc'">
              <div v-if="level.inLevel === 'Y'"
                class="title">评语：<br /></div>
              <span v-if="level.inLevel === 'Y'"
                v-html="level.scoreDesc">
              </span>
            </span>
            <br /><br />
            <hr />
          </div>
        </div>
      </div>
      <div slot="footer">
        <el-button type="primary"
          v-print="printProp"> 打 印 </el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>

export default {
  name: 'BodyReport',
  components: {},
  props: {
    reportVisible: {
      type: Boolean,
      default: false
    },
    reportData: {
      type: Array,
      default: function () {
        return [];
      }
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
    }
  },
  data () {
    return {
      dialogVisible: false,
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

    },
    onClose () {
      this.$emit('update:reportVisible', false);
    },

  }
};
</script>

<style scoped>
.line .item-title {
    font-size: 20px;
    font-weight: bold;
}
.line > div {
    display: inline-block;
    width: 100px;
}
.line .bar {
    height: 10px;
    border-radius: 10px;
}
.line .score {
    position: relative;
    left: -10px;
    top: 14px;
}
.line .name {
    position: relative;
    left: 40px;
}
.line .tag {
    position: relative;
    top: 8px;
    font-size: 1.5em;
}
.line .tag span {
    position: relative;
}
.line .desc .title {
    color: darkgreen;
    font-weight: bold;
    margin-bottom: 5px;
}
.line .desc span {
    font-size: 14px;
    line-height: 20px;
}
hr {
    margin-top: 10px;
    margin-bottom: 10px;
}
div >>> .el-dialog__header {
    background-color: #eeeeee;
    font-weight: bold;
}
.el-form-item {
    width: 200px;
}
div >>> .el-form-item__label {
    font-weight: bold;
}
#printMe {
    -webkit-print-color-adjust: exact;
}
</style>

