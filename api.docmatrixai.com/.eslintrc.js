export default {
    env: {
        node: true,
        es2021: true,
        jest: true
    },
    extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended'
    ],
    parser: '@typescript-eslint/parser',
    parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module'
    },
    plugins: [
        '@typescript-eslint'
    ],
    rules: {
        '@typescript-eslint/no-require-imports': 'error',
        'camelcase': ['error', {
            allow: [
                'exec_mode',
                'max_memory_restart',
                'error_file',
                'out_file',
                'log_date_format',
                'merge_logs',
                'log_type'
            ]
        }],
        '@typescript-eslint/no-unused-vars': ['error', {
            'argsIgnorePattern': '^_',
            'varsIgnorePattern': '^_'
        }]
    },
    overrides: [
        {
            files: ['ecosystem.config.js'],
            rules: {
                'camelcase': 'off'
            }
        }
    ]
}; 