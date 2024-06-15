import { getReportApi } from '@/api/report';
import { Button } from '@/components/ui/button';
import { IconFidgetSpinner } from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { LucideFile } from 'lucide-react';
import React from 'react';
import Plot from 'react-plotly.js';
import { useParams } from 'react-router-dom';

const ReportPreviewPage = () => {
  const params = useParams();
  console.log(params.reportId);

  const { data: reportData, isLoading: reportDataLoading } = useQuery({
    queryKey: ['reports', params.reportId],
    enabled: !!params.reportId,
    queryFn: async () => {
      return getReportApi({ id: params.reportId as string });
    },
  });
  console.log({ reportData });

  const generateAiReport = (blockId: number) => {
    // todo
  };

  return (
    <div>
      <div className="max-w-lg">
        <h3 className="text-gray-800 text-xl font-bold sm:text-2xl">
          Отчет #{params.reportId}
        </h3>
      </div>
      <div className="my-8">
        {reportDataLoading ? (
          <div>
            <IconFidgetSpinner className=" animate-spin" />
          </div>
        ) : (
          <div className="space-y-2">
            <div>
              <p className="font-bold">Запрос</p>
              <p>{reportData.search_query}</p>
            </div>
            <div>
              <p className="font-bold">Дата</p>
              <p>
                {Intl.DateTimeFormat('ru-RU').format(new Date(reportData.date))}
              </p>
            </div>
            <div>
              <p className="font-bold">Отчет</p>
              <div className="space-y-2">
                {reportData.blocks.map((block) => (
                  <div key={block.id}>
                    <Plot
                      data={block.representation.data}
                      layout={block.representation.layout}
                    />
                    <Button onClick={() => generateAiReport(block.id)}>
                      Вывод от нейросети
                    </Button>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <p className="font-bold">Скачать отчет</p>
              <div className="">
                <a
                  href="#"
                  className="hover:underline flex items-center space-x-2 mt-2"
                >
                  <LucideFile />
                  <span>отчет.pdf</span>
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ReportPreviewPage;
