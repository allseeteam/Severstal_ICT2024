import { BASE_URL } from '.';

export interface AuthParams {
  username: string;
  password: string;
}

export const authApi = async ({ username, password }: AuthParams) => {
  const response = await fetch(`${BASE_URL}/auth/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username,
      password,
    }),
  });
  const result = await response.json();
  if (response.status !== 200) {
    throw Error('Wrong credentials or server error');
  }
  return result;
};
