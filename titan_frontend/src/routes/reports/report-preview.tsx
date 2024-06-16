import {
  addCommentByBlockApi,
  downloadReportApi,
  generateSummaryByReportBlockApi,
  getReportApi,
} from '@/api/report';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { IconFidgetSpinner } from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { LucideFile, LucideMoveUp } from 'lucide-react';
import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import { useParams } from 'react-router-dom';

const ReportPreviewPage = () => {
  const params = useParams();
  console.log(params.reportId);

  const {
    data: reportData,
    isLoading: reportDataLoading,
    refetch,
  } = useQuery({
    queryKey: ['reports', params.reportId],
    enabled: !!params.reportId,
    queryFn: async () => {
      return getReportApi({ id: params.reportId as string });
    },
  });
  console.log({ reportData });

  const [summaryByBlockLoading, setSummaryByBlockLoading] = useState<any>({});

  const generateAiReport = async (blockId: number) => {
    setSummaryByBlockLoading({ ...summaryByBlockLoading, [blockId]: true });
    await generateSummaryByReportBlockApi({
      id: blockId,
      type: 'yandexgpt',
    });
    setSummaryByBlockLoading({ ...summaryByBlockLoading, [blockId]: false });
    refetch();
  };

  const downloadReport = async (type: string) => {
    const resp = await downloadReportApi({ id: reportData.id, type });
    const file = await resp.blob();
    const URL = window.URL || window.webkitURL;
    console.log({ file });
    const downloadUrl = URL.createObjectURL(file);

    const a = document.createElement('a');
    // safari doesn't support this yet
    if (typeof a.download === 'undefined') {
      window.location.href = downloadUrl;
    } else {
      a.href = downloadUrl;
      let format = 'pdf';
      if (type === 'msword') {
        format = 'docx';
      } else if (
        type === 'vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      ) {
        format = 'xls';
      }
      a.download = `Отчет ${reportData.id}.${format}`;
      document.body.appendChild(a);
      a.click();
    }

    setTimeout(function () {
      URL.revokeObjectURL(downloadUrl);
    }, 100);
    console.log({ file, downloadUrl });
  };

  const [open, setOpen] = useState(false);

  const [comment, setComment] = useState('');

  const addComment = async (blockId: number) => {
    if (!comment) {
      return;
    }
    await addCommentByBlockApi({ id: blockId, comment });
    setOpen(false);
    setComment('');
    refetch();
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
            <div className="max-w-xl">
              <p className="font-bold">Отчет</p>
              <div className="space-y-2">
                {reportData.blocks.map((block) => (
                  <div key={block.id}>
                    {block.type === 'text' ? (
                      <div>{block.representation.text}</div>
                    ) : (
                      <Plot
                        data={block.representation.data}
                        layout={block.representation.layout}
                      />
                    )}
                    <div className="flex flex-col space-y-2 items-end">
                      <div>
                        <a
                          href={block.source}
                          target="_blank"
                          className="hover:underline"
                        >
                          Источник: {block.source}
                        </a>
                      </div>
                      {!block.summary ? (
                        <Button
                          onClick={() => generateAiReport(block.id)}
                          className="w-fit"
                          disabled={summaryByBlockLoading[block.id]}
                        >
                          {summaryByBlockLoading[block.id] ? (
                            <div className="flex items-center justify-center mt-4">
                              <IconFidgetSpinner
                                className=" animate-spin"
                                size={16}
                              />
                            </div>
                          ) : (
                            'Вывод от нейросети'
                          )}
                        </Button>
                      ) : null}
                      {!block.comment ? (
                        <Dialog open={open} onOpenChange={setOpen}>
                          <DialogTrigger asChild>
                            <Button onClick={() => {}} className="w-fit">
                              Добавить комментарий
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="sm:max-w-[425px]">
                            <DialogHeader>
                              <DialogTitle>Комментарий к блоку</DialogTitle>
                            </DialogHeader>
                            <div>
                              <div className="grid grid-cols-2 items-start gap-2 p-4 border rounded-lg">
                                <Label htmlFor="name" className="text-left">
                                  Комментарий
                                </Label>
                                <Input
                                  id="name"
                                  defaultValue=""
                                  className="col-span-3"
                                  value={comment}
                                  onChange={(e) => setComment(e.target.value)}
                                />
                              </div>
                              <div className="flex justify-end">
                                <Button
                                  onClick={() => addComment(block.id)}
                                  className="mt-4 "
                                >
                                  Добавить комментарий
                                </Button>
                              </div>
                            </div>
                          </DialogContent>
                        </Dialog>
                      ) : null}
                    </div>
                    {block.comment ? (
                      <div className="my-4 border rounded-md p-4">
                        <p className="font-bold">
                          Комментарий к блоку{' '}
                          <LucideMoveUp className="inline" size={16} />
                        </p>
                        <div className="my-2 text-xs">{block.comment}</div>
                      </div>
                    ) : null}
                    {block.summary ? (
                      <div className="my-4 border rounded-md p-4">
                        <p className="font-bold">
                          Суммаризация блока от ИИ{' '}
                          <LucideMoveUp className="inline" size={16} />
                        </p>
                        <div
                          dangerouslySetInnerHTML={{ __html: block.summary }}
                          className="my-2 text-xs"
                        ></div>
                      </div>
                    ) : null}
                  </div>
                ))}
              </div>
            </div>
            <div>
              <p className="font-bold">Скачать отчет</p>
              <div className="space-y-2">
                <a
                  onClick={() => downloadReport('pdf')}
                  href="javascript:void(0);"
                  className="hover:underline flex items-center space-x-2 mt-2"
                >
                  <LucideFile />
                  <span>Отчет {reportData.id}.pdf</span>
                </a>
                <a
                  onClick={() => downloadReport('msword')}
                  href="javascript:void(0);"
                  className="hover:underline flex items-center space-x-2 mt-2"
                >
                  <LucideFile />
                  <span>Отчет {reportData.id}.docx</span>
                </a>
                <a
                  onClick={() =>
                    downloadReport(
                      'vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                  }
                  href="javascript:void(0);"
                  className="hover:underline flex items-center space-x-2 mt-2"
                >
                  <LucideFile />
                  <span>Отчет {reportData.id}.xls</span>
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
