import React, { useState } from 'react';
import { DebouncedInput } from '../../components/reports-table';
import { IconFidgetSpinner } from '@tabler/icons-react';
import { Button } from '@/components/ui/button';
import { useQuery } from '@tanstack/react-query';
import { getThemesApi } from '@/api/theme';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { TemplateCard } from '@/components/template-card';
import { LucidePlusSquare } from 'lucide-react';
import { TemplateModal } from '@/components/template-modal';
import { PostTemplateParams, postTemplateApi } from '@/api/template';
import { postReportApi } from '@/api/report';
import { useNavigate } from 'react-router-dom';
import { Input } from '@/components/ui/input';

const ReportsCreatePage = () => {
  const {
    data: themesData,
    isLoading: themesDataLoading,
    refetch: refetchThemes,
  } = useQuery({
    queryKey: ['themes'],
    queryFn: async () => {
      return getThemesApi({ page: 1 });
    },
  });
  console.log({ themesData });
  const [selectedTheme, setSelectedTheme] = useState<number>(1);
  const [selectedTemplate, setSelectedTemplate] = useState(0);
  console.log({ selectedTheme });

  const templatesByTheme = themesData?.results
    ? themesData.results.find((v: any) => v.id === selectedTheme)?.templates
    : [];

  const onTemplateCreated = async (params: {
    name: string;
    query_template: string[];
  }) => {
    if (!selectedTheme) {
      console.error('no theme chosen');
      return;
    }
    const templateParams = {
      theme: selectedTheme,
      name: params.name,
      meta_blocks: params.query_template.map((v, i) => ({
        query_template: v,
        position: i,
      })),
    };
    await postTemplateApi(templateParams);
    setTimeout(() => {
      refetchThemes();
    }, 200);
  };

  const navigate = useNavigate();

  const [searchQuery, setSearchQuery] = useState('');
  const [reportsLoading, setReportsLoading] = useState(false);

  const generateReport = async () => {
    if (!selectedTemplate) {
      console.error('no template chosen');
      return;
    }
    setReportsLoading(true);

    const report = await postReportApi({
      template: selectedTemplate,
      search_query: searchQuery,
    });
    console.log({ report });
    setReportsLoading(false);
    setTimeout(() => {
      navigate(`/reports/${report.id}`);
    }, 200);
  };

  return (
    <div>
      <h3 className="text-gray-800 text-xl font-bold sm:text-2xl">
        Генерация отчета
      </h3>
      <div className="flex items-start justify-between space-x-8 mt-4">
        <div className="w-[60%]">
          <p className="text-sm font-bold">
            1. Выберите тематику для начала генерации:
          </p>
          {themesDataLoading ? (
            <div className="flex items-center justify-center mt-4">
              <IconFidgetSpinner className=" animate-spin" />
            </div>
          ) : (
            <div className="mt-2 w-full">
              {themesData.count && themesData.results?.length ? (
                <Select value={selectedTheme} onValueChange={setSelectedTheme}>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Тематика отчета..." />
                  </SelectTrigger>
                  <SelectContent>
                    {themesData.results.map((theme: any) => (
                      <SelectItem key={theme.id} value={theme.id}>
                        {theme.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              ) : (
                <div>No theme data</div>
              )}
            </div>
          )}

          <div className="mt-4">
            <p className="text-sm font-bold">2. Введите поисковой запрос</p>
            <div className="mt-2 w-full">
              <Input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="font-lg shadow border border-block"
                placeholder="Предприятия в банковском секторе..."
              />
            </div>
            {/* <section className="bg-white border rounded-xl mt-2">
              <div className="py-4 px-4 mx-auto max-w-screen-xl">
                <div className="flex items-center justify-center">
                  <IconFidgetSpinner className=" animate-spin" />
                </div>
                <div className="flex items-center justify-end">
                  <Button className="border">Продолжить</Button>
                </div>
              </div>
            </section> */}
          </div>
          <div className="mt-4">
            <p className="text-sm font-bold">
              3. Выберите шаблон или создайте новый
            </p>
            <div className="mt-4 w-full">
              <div className="grid grid-cols-2 xl:grid-cols-3 gap-2">
                {templatesByTheme?.length
                  ? templatesByTheme.map((template: any) => (
                      <TemplateCard
                        key={template.id}
                        title={template.name}
                        description=""
                        blocks={template.meta_blocks}
                        className="cursor-pointer hover:text-card-foreground hover:shadow min-w-[220px]"
                        checked={selectedTemplate === template.id}
                        onClick={() => {
                          setSelectedTemplate(template.id);
                        }}
                      />
                    ))
                  : null}
                <TemplateModal onTemplateCreated={onTemplateCreated}>
                  <div className="rounded-lg border bg-card text-card-foreground/80 hover:text-card-foreground shadow-sm hover:shadow w-full cursor-pointer flex flex-col space-y-2 items-center justify-center p-4">
                    <LucidePlusSquare size={48} />
                    <p className="text-sm">Создать новый шаблон</p>
                  </div>
                </TemplateModal>
              </div>
            </div>
          </div>
          <div className="mt-4 flex justify-end mb-4">
            <Button onClick={generateReport} disabled={reportsLoading}>
              {reportsLoading ? (
                <div className="flex items-center justify-center mt-4">
                  <IconFidgetSpinner className=" animate-spin" size={16} />
                </div>
              ) : (
                'Сгенерировать отчет'
              )}
            </Button>
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
