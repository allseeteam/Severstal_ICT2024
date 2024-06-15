import { BASE_URL } from '.';

export interface PostTemplateParams {
  theme: number;
  name: string;
  meta_blocks: {
    query_template: string;
    position: number;
  }[];
}

export const postTemplateApi = async (params: PostTemplateParams) => {
  const lsToken = localStorage.getItem('test-auth') || '';
  const token = lsToken.slice(1, lsToken?.length - 1);
  const response = await fetch(`${BASE_URL}/template/`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Token ' + token,
    },
    body: JSON.stringify(params),
  });
  const result = await response.json();
  if (response.status === 401) {
    localStorage.removeItem('test-auth');
    throw Error('Wrong credentials or server error');
  }
  return result;
};
