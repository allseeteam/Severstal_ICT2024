import { Checkbox } from '@/components/ui/checkbox';
import React from 'react';

const PreferencesPage = () => {
  const layoutChoice = [
    {
      id: 'graphs',
      title: 'Графики',
    },
    {
      id: 'tables',
      title: 'Таблицы',
    },
    {
      id: 'text',
      title: 'Текст',
    },
  ];

  return (
    <div>
      <h3 className="text-gray-800 text-xl font-bold sm:text-2xl">
        Пользовательские настройки
      </h3>
      <div className="mt-4">
        <p className="font-bold">Тематики исследований</p>
        <p className="font-bold mt-4">Предпочтительный формат отчетов</p>
        {layoutChoice.map((v) => (
          <div className="items-center flex space-x-2 mt-2">
            <Checkbox id={v.id} />
            <div className="grid gap-1.5 leading-none">
              <label
                htmlFor={v.id}
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                {v.title}
              </label>
            </div>
          </div>
        ))}
        <p className="font-bold mt-4">Предпочтительные источники данных</p>
      </div>
    </div>
  );
};

export default PreferencesPage;
