import { FilePieChart } from 'lucide-react';
import { Link } from 'react-router-dom';
import useScroll from '../utils/hooks/use-scroll';
import { cn } from '@/utils';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

const Header = () => {
  const scrolled = useScroll(50);

  return (
    <header
      className={cn(
        'z-[50] fixed top-0 w-full bg-transparent  transition-all border-b border-border/40 ',
        scrolled ? 'bg-white/20 backdrop-blur-lg' : 'bg-white/0 '
      )}
      style={{ transform: 'none' }}
    >
      <div className="block">
        <div className="container flex h-16 items-center max-w-[88rem] mx-auto">
          <div className="mr-4 flex">
            <Link
              className="flex items-center justify-center space-x-2 text-2xl py-6 text-center transition-colors text-foreground mr-10"
              to="/"
            >
              <FilePieChart size={26} />
              <div className="flex flex-col">
                <h1 className="text-lg text-left font-semibold">ТА-Сервис</h1>
              </div>
            </Link>
          </div>
          <nav className="flex items-center space-x-6 text-sm font-medium xl:flex">
            <Link
              to="/reports"
              className="transition-colors hover:text-foreground group  text-foreground/80 hidden sm:flex space-x-1"
            >
              <span className="group-hover:underline">Отчеты</span>
              <span className="ml-2 flex items-center justify-start h-full rounded-md border border-blue-d2 text-blue-d2 px-1.5 py-0.5 text-xs leading-none no-underline group-hover:no-underline">
                new
              </span>
            </Link>
            {/* <Link
              className="transition-colors hover:text-foreground hover:underline text-foreground/80 hidden sm:flex space-x-1"
              to="/sources"
            >
              Источники
            </Link> */}
            <Link
              className="transition-colors hover:text-foreground hover:underline text-foreground/80 hidden sm:flex space-x-1"
              to="/generate"
            >
              Генерация
            </Link>
          </nav>
          <div className="flex flex-1 items-center justify-end gap-2 sm:gap-2 md:justify-end">
            <Link
              to="/support"
              className="transition-colors hover:underline hover:text-foreground text-foreground/80 mr-3 text-sm font-medium"
            >
              <span className="hidden sm:block">Помощь</span>
            </Link>
            {/* <button className="sm:flex relative hidden justify-start items-center text-sm text-muted-foreground dark:border-white/[0.2] py-2 w-fit border border-transparent shadow-[0px_2px_3px_-1px_rgba(0,0,0,0.1),0px_1px_0px_0px_rgba(25,28,33,0.02),0px_0px_0px_1px_rgba(25,28,33,0.08)] px-4 rounded-xl bg-white dark:bg-brand">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                className="h-4 w-4 text-neutral-500"
              >
                <path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0"></path>
                <path d="M21 21l-6 -6"></path>
              </svg>
              <span className="transition-colors hover:text-foreground text-foreground/80 text-sm font-medium pl-2 pr-4">
                Search Components
              </span>
              <kbd className="pointer-events-none hidden h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium opacity-100 sm:flex">
                <span className="text-xs">⌘</span>K
              </kbd>
            </button> */}
            <Link
              to="/preferences"
              className="relative whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-10 py-2 px-3 flex items-center justify-center outline-none focus:ring-0 focus:outline-none active:ring-0 active:outline-none"
            >
              <Avatar>
                <AvatarImage src="https://github.com/shadcn.png" />
                <AvatarFallback>TA</AvatarFallback>
              </Avatar>
              <span className="sr-only">Пользователь</span>
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
