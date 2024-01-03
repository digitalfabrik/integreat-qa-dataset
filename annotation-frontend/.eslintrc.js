module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint', 'jsx-expressions', 'prefer-arrow', 'react', 'react-hooks'],
  extends: [
    'airbnb',
    'airbnb/hooks',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  env: {
    es6: true,
    node: true,
    browser: true,
  },
  ignorePatterns: ['reports/', 'node_modules/', 'dist/', '/.eslintrc.js'],
  rules: {
    // Unwanted
    'lines-between-class-members': 'off',
    'import/extensions': 'off',
    'import/named': 'off',
    'import/prefer-default-export': 'off',
    'import/no-named-as-default-member': 'off',
    'react/require-default-props': 'off',
    'react/sort-comp': 'off',

    // Disabling since better @typescript-eslint rules available or they make no sense for ts projects
    'default-case': 'off',
    'no-use-before-define': 'off',
    'import/no-unresolved': 'off',
    'react/jsx-filename-extension': 'off',

    curly: ['error', 'all'],
    'func-names': 'error',
    'no-console': 'error',
    'no-magic-numbers': [
      'error',
      {
        ignore: [-1, 0, 1, 2],
        ignoreArrayIndexes: true,
      },
    ],
    'prefer-destructuring': ['error', { array: false }],
    'prefer-object-spread': 'error',

    'react/function-component-definition': [
      'error',
      {
        namedComponents: 'arrow-function',
        unnamedComponents: 'arrow-function',
      },
    ],
    'react/jsx-no-useless-fragment': ['error', { allowExpressions: true }],
    'react/no-did-mount-set-state': 'error',
    'react/no-unused-prop-types': 'warn',
    'react-hooks/exhaustive-deps': 'error',

    '@typescript-eslint/await-thenable': 'error',
    '@typescript-eslint/ban-ts-comment': 'error',
    '@typescript-eslint/consistent-type-definitions': ['error', 'type'],
    '@typescript-eslint/explicit-module-boundary-types': 'error',
    '@typescript-eslint/no-empty-function': 'error',
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-unnecessary-condition': 'error',
    '@typescript-eslint/no-unused-vars': [
      'error',
      {
        argsIgnorePattern: '_(unused)?',
        varsIgnorePattern: '_(unused)?',
        ignoreRestSiblings: true,
      },
    ],
    '@typescript-eslint/no-use-before-define': 'error',
    '@typescript-eslint/prefer-ts-expect-error': 'error',
    '@typescript-eslint/switch-exhaustiveness-check': 'error',
    '@typescript-eslint/no-non-null-assertion': 'error',

    'jsx-expressions/strict-logical-expressions': 'error',

    'prefer-arrow/prefer-arrow-functions': 'error',
  },
  parserOptions: {
    project: true,
  },
  reportUnusedDisableDirectives: true,
  settings: {
    react: {
      version: 'detect',
    },
  },
}
