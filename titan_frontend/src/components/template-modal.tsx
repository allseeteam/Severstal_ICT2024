import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from '@/components/ui/select';
import { LucidePlusSquare } from 'lucide-react';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import Balancer from 'react-wrap-balancer';

function createArrayWithNumbers(length) {
  return Array.from({ length }, (_, i) => i);
}

export function TemplateModal({ children, onTemplateCreated }: any) {
  const [open, setOpen] = useState(false);
  // todo useForm dynamic
  const [size, setSize] = useState(1);
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm();

  const handleTemplateCreation = (data: any) => {
    onTemplateCreated(data);
    setOpen(false);
    reset();
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Новый шаблон</DialogTitle>
          <DialogDescription>
            <Balancer>
              Добавляйте и редактируйте блоки для шаблона отчета. По заголовкам
              блока будет формироваться содержимое отчета
            </Balancer>
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit(handleTemplateCreation)}>
          <div className="grid gap-4 overflow-auto max-h-[500px] my-4 mt-2">
            <div className="grid grid-cols-2 items-start gap-2 p-4 border rounded-lg">
              <Label htmlFor="name" className="text-left">
                Название шаблона
              </Label>
              <Input
                id="name"
                defaultValue="Z analytics"
                className="col-span-3"
                {...register('name', {
                  required: true,
                })}
              />
            </div>
            {createArrayWithNumbers(size).map((number: number) => (
              <div
                key={number}
                className="rounded-lg border bg-card text-card-foreground/80 hover:text-card-foreground shadow-sm hover:shadow w-full cursor-pointer flex flex-col space-y-2 items-center justify-center p-4"
              >
                <div className="grid grid-cols-2 items-start gap-2 w-full">
                  <Label
                    htmlFor={`query_template.${number}`}
                    className="text-left"
                  >
                    Заголовок блока {number + 1}
                  </Label>
                  <Input
                    id={`query_template.${number}`}
                    defaultValue="Объем рынка {theme}"
                    className="col-span-3"
                    {...register(`query_template.${number}`, {
                      required: true,
                    })}
                  />
                </div>
                {/* <div className="items-start gap-2 w-full">
                <Select>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Таблица" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="light">График</SelectItem>
                    <SelectItem value="dark">Таблица</SelectItem>
                    <SelectItem value="system">Текст</SelectItem>
                  </SelectContent>
                </Select>
              </div> */}
              </div>
            ))}
            <div
              onClick={() => setSize((size) => size + 1)}
              className="rounded-lg border bg-card text-card-foreground/80 hover:text-card-foreground shadow-sm hover:shadow w-full cursor-pointer flex flex-col space-y-2 items-center justify-center p-4"
            >
              <LucidePlusSquare size={24} />
              <p className="text-sm">Добавить блок</p>
            </div>
          </div>
          <DialogFooter>
            <Button type="submit">Создать шаблон</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
