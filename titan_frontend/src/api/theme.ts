import { BASE_URL } from '.';

interface GetReportParams {
  page: number;
}

export const getThemesApi = async ({ page }: GetReportParams) => {
  const lsToken = localStorage.getItem('test-auth') || '';
  const token = lsToken.slice(1, lsToken?.length - 1);
  const response = await fetch(`${BASE_URL}/theme/?page=${page}`, {
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
