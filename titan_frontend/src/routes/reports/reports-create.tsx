import React from 'react';
import { DebouncedInput } from '../../components/reports-table';
import { IconFidgetSpinner } from '@tabler/icons-react';
import { Button } from '@/components/ui/button';

const ReportsCreatePage = () => {
  return (
    <div>
      <h3 className="text-gray-800 text-xl font-bold sm:text-2xl">
        Генерация отчета
      </h3>
      <div className="flex items-start justify-between space-x-8 mt-4">
        <div className="w-[60%]">
          <p className="text-sm">1. Введите тематику для начала генерации:</p>
          <div className="mt-2">
            <DebouncedInput
              value={''}
              onChange={(value) => console.log(String(value))}
              className="font-lg shadow border border-block"
              placeholder="Поиск по тематикам..."
            />
          </div>

          <div className="my-6">
            <p className="text-sm">2. Выберите подходящие источники</p>
            <section className="bg-white border rounded-xl mt-2">
              <div className="py-4 px-4 mx-auto max-w-screen-xl">
                <div className="flex items-center justify-center">
                  <IconFidgetSpinner className=" animate-spin" />
                </div>
                <div className="flex items-center justify-end">
                  <Button className="border">Продолжить</Button>
                </div>
              </div>
            </section>
          </div>
        </div>
        <div className="w-[40%]">
          <section className="bg-white border rounded-xl">
            <div className="py-4 px-4 mx-auto max-w-screen-xl sm:py-8 lg:px-6">
              <p>Секция с инструкцией</p>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default ReportsCreatePage;
