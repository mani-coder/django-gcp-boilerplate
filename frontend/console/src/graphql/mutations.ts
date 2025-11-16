import { gql } from 'urql'

export const LOGIN_MUTATION = gql`
  mutation Login($code: String!) {
    login(code: $code) {
      responseCode
      token
      user {
        id
        email
        firstName
        lastName
      }
    }
  }
`
