import React, { useEffect, useState } from 'react';
import { ReportsTable } from '../../components/reports-table';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import Balancer from 'react-wrap-balancer';

const ReportsPage = () => {
  return (
    <div>
      <div className="flex justify-between items-center">
        <div className="max-w-lg">
          <h3 className="text-gray-800 text-xl font-bold sm:text-2xl">
            Отчеты
          </h3>
          <p className="text-gray-600 text-sm mt-2">
            <Balancer>
              На этой странице можно посмотреть список сгенерированных отчетов
              по запросам, найти нужный по параметрам и перейти на детальную
              страницу отчета
            </Balancer>
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
