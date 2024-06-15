import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { cn } from '@/utils';

type CardProps = React.ComponentProps<typeof Card> & {
  description: string;
  title: string;
  checked: boolean;
  blocks: {
    id: number;
    position: number;
    query_template: string;
  }[];
};

export function TemplateCard({
  className,
  title,
  description,
  blocks,
  checked = true,
  ...props
}: CardProps) {
  return (
    <Card
      className={cn(
        'w-full relative',
        checked ? 'border-black/40' : '',
        className
      )}
      {...props}
    >
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4">
        <div>
          {checked ? (
            <div className="absolute top-1 right-1 rounded-md border p-2 text-xs">
              Выбран
            </div>
          ) : null}
          {blocks.map((block) => (
            <div
              key={block.id}
              className="mb-4 grid grid-cols-[25px_1fr] items-start pb-4 last:mb-0 last:pb-0"
            >
              <span className="flex h-2 w-2 translate-y-1 rounded-full bg-sky-500" />
              <div className="space-y-1">
                <p className="text-sm font-medium leading-none">
                  {block.query_template}
                </p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
