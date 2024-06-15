import { BASE_URL } from '.';

export interface GetReportParams {
  page: number;
}

export const getReportsApi = async ({ page }: GetReportParams) => {
  const lsToken = localStorage.getItem('test-auth') || '';
  const token = lsToken.slice(1, lsToken?.length - 1);
  const response = await fetch(`${BASE_URL}/report/?page=${page}`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Token ' + token,
    },
  });
  const result = await response.json();
  if (response.status === 401) {
    localStorage.removeItem('test-auth');
    throw Error('Wrong credentials or server error');
  }
  return result;
};

export const getReportApi = async ({ id }: { id: string }) => {
  const lsToken = localStorage.getItem('test-auth') || '';
  const token = lsToken.slice(1, lsToken?.length - 1);
  const response = await fetch(`${BASE_URL}/report/${id}/`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Token ' + token,
    },
  });
  const result = await response.json();
  if (response.status === 401) {
    localStorage.removeItem('test-auth');
    throw Error('Wrong credentials or server error');
  }
  return result;
};

interface PostTemplateParams {
  template: number;
  search_query: string;
}

export const postReportApi = async (params: PostTemplateParams) => {
  const lsToken = localStorage.getItem('test-auth') || '';
  const token = lsToken.slice(1, lsToken?.length - 1);
  const response = await fetch(`${BASE_URL}/report/`, {
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