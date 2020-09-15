module.exports = {
  root: true,
  parserOptions: {
    parser: 'babel-eslint',
    sourceType: 'module'
  },
  globals: {
    "$": true,
    "jQuery": true
  },
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/recommended'
  ],
  // required to lint *.vue files
  plugins: [
    'vue'
  ],
  // add your custom rules here
  rules: {
    'no-prototype-builtins': 'off',
    // allow async-await
    'generator-star-spacing': 'off',
    // allow debugger during development
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'indent': 'off',
    // 'indent': ['error', 2],
    'vue/script-indent': [
      'error', 2, {
        'baseIndent': 1,
        'switchCase': 0,
        'ignores': []
      }
    ],
    'vue/max-attributes-per-line': [
      2,
      {
        'singleline': 10,
        'multiline': {
          'max': 1,
          'allowFirstLine': true
        }
      }
    ],
    'vue/html-self-closing': [
      'error', {
        'html': {
          'void': 'any',
          'normal': 'any',
          'component': 'any'
        },
        'svg': 'any',
        'math': 'any'
      }
    ],
    'no-new': 0,
    'no-unused-vars': [
      'error', {
        'vars': 'local',
        'args': 'none'
      }],
    'vue/no-use-v-if-with-v-for': ['error', {
      allowUsingIterationVar: true
    }],
    'prefer-promise-reject-errors': ["error", {
      allowEmptyReject: true
    }],
    'space-before-function-paren': 0,
    'object-property-newline': 0,
    'semi': ['error', 'always'],
    'brace-style': 'error',
    'object-curly-spacing': ['error', 'always'],
    quotes: [2, 'single'],
    curly: 'error',
    'keyword-spacing': ['error', { 'before': true, 'after': true }],
    'space-before-blocks': 'error',
    'space-infix-ops': 'error',
    'no-trailing-spaces': 'error'
  }
};
