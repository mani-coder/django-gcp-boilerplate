import { CodegenConfig } from '@graphql-codegen/cli'

const config: CodegenConfig = {
  schema: 'src/gql/schema.graphql',
  documents: ['src/**/*.{ts,tsx}'],
  generates: {
    './src/__generated__/': {
      preset: 'client',
      config: {
        withHooks: true,
        withHOC: false,
        withComponent: false,
        skipTypename: true,
        skipTypeNameForRoot: true,
        enumsAsTypes: true, // This generates enums as string union types
        useTypeImports: true, // Use type-only imports for TypeScript
        scalars: {
          JSONString: 'string',
          Date: 'string',
          DateTime: 'string',
        },
      },
    },
  },
  hooks: {
    afterAllFileWrite: ['prettier --write'],
  },
}

export default config
