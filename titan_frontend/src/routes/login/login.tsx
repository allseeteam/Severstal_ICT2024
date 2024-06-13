import React from 'react';
import { SignupFormDemo } from '../../components/login-form';

const LoginPage = () => {
  return (
    <div className="h-screen">
      <div className="h-full flex items-center -mt-20">
        <SignupFormDemo />
      </div>
    </div>
  );
};

export default LoginPage;
