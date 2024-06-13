import { AuthParams, authApi } from '@/api/auth';
import { sleep } from '../utils';

const fakeAuthProvider = {
  isAuthenticated: false,
  async signin({ username, password }: AuthParams, callback: VoidFunction) {
    fakeAuthProvider.isAuthenticated = true;
    const response = await authApi({ username, password });
    console.log({ response });
    await sleep(1500); // fake async
    callback();
  },
  async signout(callback: VoidFunction) {
    fakeAuthProvider.isAuthenticated = false;
    await sleep(1500);
    callback();
  },
};

export { fakeAuthProvider };
