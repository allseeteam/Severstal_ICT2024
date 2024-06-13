import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './header';

const Layout = () => {
  return (
    <div className="min-h-screen h-full flex flex-col items-stretch relative">
      <Header />
      <div className="h-full absolute w-full -z-10 bg-grid-black/[0.1] flex items-center justify-center">
        {/* Radial gradient for the container to give a faded look */}
        <div className="absolute pointer-events-none inset-0 flex items-center justify-center bg-blue-d1 [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]"></div>
      </div>

      <main className="container w-full pt-20 h-full">
        {/* <AuthStatus /> */}

        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
