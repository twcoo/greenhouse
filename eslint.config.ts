import { defineConfig } from "eslint/config"
import tsParser from "@typescript-eslint/parser"
import pluginTs from "@typescript-eslint/eslint-plugin"
import pluginVue from "eslint-plugin-vue"
import pluginOxlint from "eslint-plugin-oxlint"

export default defineConfig([
  {
    ignores: ["dist", "coverage", "node_modules", "frontend/src/components/ui"]
  },

  {
    files: ["frontend/src/**/*.{ts,tsx}"],

    languageOptions: {
      parser: tsParser,
    },

    plugins: {
      "@typescript-eslint": pluginTs,
    },

    rules: {
      "@typescript-eslint/consistent-type-assertions": "error",
      "complexity": ["warn", { max: 10 }],
      "no-restricted-syntax": [
        "error",
        {
          selector: "TSEnumDeclaration",
          message: "Use literal unions or `as const` objects instead of enums.",
        },
        {
          selector: "IfStatement > IfStatement.alternate",
          message: "Avoid `else if`. Prefer early returns or ternary operators.",
        },
        {
          selector: "IfStatement > :not(IfStatement).alternate",
          message: "Avoid `else`. Prefer early returns or ternary operators.",
        },
        {
          selector: "TryStatement",
          message:
            "Use tryCatch() from @/lib/tryCatch instead of try/catch. Returns Result<T> tuple: [error, null] | [null, data].",
        },
      ],
    },
  },

  {
    files: ["frontend/src/**/*.vue"],

    languageOptions: {
      parser: (await import("vue-eslint-parser")).default,
      parserOptions: {
        parser: tsParser,
        ecmaVersion: "latest",
        sourceType: "module",
        extraFileExtensions: [".vue"],
      },
    },

    plugins: {
      vue: pluginVue,
    },

    rules: {
      'vue/multi-word-component-names': ['error', { ignores: ['App', 'Layout'] }],
      'vue/component-name-in-template-casing': ['error', 'PascalCase'],
      'vue/prop-name-casing': ['error', 'camelCase'],
      'vue/custom-event-name-casing': ['error', 'kebab-case'],
      'vue/no-unused-properties': ['error', { groups: ['props', 'data', 'computed', 'methods'] }],
      'vue/no-unused-refs': 'error',
      'vue/define-props-destructuring': 'error',
      'vue/prefer-use-template-ref': 'error',
      'vue/max-template-depth': ['error', { maxDepth: 8 }],
      'vue/no-unused-properties': ['error', {
        groups: ['props', 'data', 'computed', 'methods']
      }],
      'vue/no-unused-refs': 'error',
      'vue/no-unused-emit-declarations': 'error'
    },
  },

  ...pluginOxlint.buildFromOxlintConfigFile("./.oxlintrc.json"),
])
