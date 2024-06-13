import React from 'react';
import { ReportsTable } from '../../components/reports-table';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';

const ReportsPage = () => {
  return (
    <div>
      <div className="flex justify-between items-center">
        <div className="max-w-lg">
          <h3 className="text-gray-800 text-xl font-bold sm:text-2xl">
            Отчеты
          </h3>
          <p className="text-gray-600 mt-2">
            Lorem Ipsum is simply dummy text of the printing and typesetting
            industry.
          </p>
        </div>
        <div>
          <Button asChild>
            <Link to="/generate">Сгенерировать отчет</Link>
          </Button>
        </div>
      </div>
      <ReportsTable />
    </div>
  );
};

export default ReportsPage;
