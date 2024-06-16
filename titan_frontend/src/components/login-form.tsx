'use client';
import React, { useState } from 'react';
import { Label } from './ui/label';
import { Input } from './ui/input';
import { cn } from '@/utils';
import { useAuth } from './auth-provider';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useLocation, useNavigate } from 'react-router-dom';
import { IconFidgetSpinner } from '@tabler/icons-react';
import { Button } from './ui/button';
import Balancer from 'react-wrap-balancer';

type Inputs = {
  login: string;
  password: string;
};

export function SignupFormDemo() {
  const auth = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const [isSubmitting, setIsSubmitting] = useState(false);
  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    setIsSubmitting(true);
    console.log('Form submitted');
    console.log({ location });
    await auth.signin({ username: data.login, password: data.password });
    setIsSubmitting(false);
    navigate(location.state?.from?.pathname ?? '/');
  };
  return (
    <div className="max-w-md w-full mx-auto rounded-none md:rounded-2xl p-4 md:p-8 shadow-input bg-blue-d1 border">
      <h2 className="font-bold text-xl text-black-d1">Добро пожаловать</h2>
      <p className="text-black-d2 text-sm max-w-sm mt-2">
        <Balancer>
          Доступ через логин/пароль, который вам выдали (для тестирования: логин
          - test, пароль - test)
        </Balancer>
      </p>

      <form className="mt-4 mb-2" onSubmit={handleSubmit(onSubmit)}>
        <LabelInputContainer className="mb-4">
          <Label>Логин</Label>
          <Input
            placeholder="project@tas.ru"
            {...register('login', { required: true })}
          />
          <div className="!mt-0">
            {errors.login && <span className="text-xs">Введите данные</span>}
          </div>
        </LabelInputContainer>
        <LabelInputContainer className="mb-4">
          <Label htmlFor="password">Пароль</Label>
          <Input
            id="password"
            placeholder="••••••••"
            type="password"
            {...register('password', { required: true })}
          />
          <div className="!mt-0">
            {errors.password && <span className="text-xs">Введите данные</span>}
          </div>
        </LabelInputContainer>

        <Button className="w-full mt-2" type="submit" disabled={isSubmitting}>
          {isSubmitting ? (
            <div className="flex items-center justify-center">
              <IconFidgetSpinner className=" animate-spin" />
            </div>
          ) : (
            <span>Войти &rarr;</span>
          )}
        </Button>

        {/* <div className="bg-gradient-to-r from-transparent via-neutral-400 to-transparent my-8 h-[1px] w-full" /> */}
      </form>
    </div>
  );
}

const LabelInputContainer = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return (
    <div className={cn('flex flex-col space-y-2 w-full', className)}>
      {children}
    </div>
  );
};
