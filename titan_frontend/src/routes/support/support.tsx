import { LucideMessageCircleQuestion } from 'lucide-react';
import React from 'react';

const SupportPage = () => {
  return (
    <div className="my-10">
      <section className="bg-white border rounded-xl">
        <div className="py-4 px-4 mx-auto max-w-screen-xl sm:py-8 lg:px-6">
          <h2 className="mb-8 text-4xl tracking-tight font-extrabold text-gray-900 ">
            Часто задаваемые вопросы
          </h2>
          <div className="grid pt-8 text-left border-t border-gray-200 md:gap-16 md:grid-cols-2">
            <div>
              <div className="mb-10">
                <h3 className="flex items-center mb-4 text-lg font-medium text-gray-900 ">
                  <LucideMessageCircleQuestion size={24} className="mr-2" />
                  Как сгенерировать отчет?
                </h3>
                <p className="text-gray-500 ">
                  Заполните все пункты на странице генерации и нажмите кнопку
                  сгенерировать отчет
                </p>
              </div>
              <div className="mb-10">
                <h3 className="flex items-center mb-4 text-lg font-medium text-gray-900 ">
                  <LucideMessageCircleQuestion size={24} className="mr-2" />
                  Что значит "вывод от нейросети" в отчете?
                </h3>
                <p className="text-gray-500 ">
                  Это суммаризация LLM моделью информации в блоке отчета
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default SupportPage;
