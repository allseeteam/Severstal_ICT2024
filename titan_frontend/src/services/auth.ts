import { AuthParams, authApi } from '@/api/auth';
import { sleep } from '../utils';

const fakeAuthProvider = {
  isAuthenticated: false,
  async signin(
    { username, password }: AuthParams,
    callback: (token: string) => void,
    errCallback: (error: any) => void
  ) {
    fakeAuthProvider.isAuthenticated = true;
    try {
      const response = await authApi({ username, password });
      console.log({ response });
      await sleep(1500); // fake async
      callback(response.token);
    } catch (err) {
      console.error(err);
      errCallback('Wrong credentials or server error');
    }
  },
  async signout(callback: VoidFunction) {
    fakeAuthProvider.isAuthenticated = false;
    await sleep(1500);
    callback();
  },
};

export { fakeAuthProvider };
