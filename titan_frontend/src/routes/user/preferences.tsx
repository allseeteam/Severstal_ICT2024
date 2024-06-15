import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import React, { useEffect, useState } from 'react';

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

  const [checkedIds, setCheckedIds] = useState({
    graphs: false,
    tables: false,
    text: false,
  });

  useEffect(() => {
    const pref = localStorage.getItem('user-preferences');
    if (pref) {
      setCheckedIds(JSON.parse(pref));
    }
  }, []);

  const savePreferences = () => {
    localStorage.setItem('user-preferences', JSON.stringify(checkedIds));
  };

  return (
    <div>
      <h3 className="text-gray-800 text-xl font-bold sm:text-2xl">
        Пользовательские настройки
      </h3>
      <div className="mt-4">
        <p className="font-bold mt-4">Предпочтительный формат отчетов</p>
        {layoutChoice.map((v) => (
          <div className="items-center flex space-x-2 mt-2">
            <Checkbox
              key={v.id}
              id={v.id}
              checked={!!checkedIds[v.id]}
              onCheckedChange={(val) => {
                setCheckedIds({ ...checkedIds, [v.id]: val });
              }}
            />
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
        <Button onClick={savePreferences} className="my-4">
          Сохранить
        </Button>
      </div>
    </div>
  );
};

export default PreferencesPage;
