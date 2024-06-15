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
      <div className="hidden md:block">
        <div className="container flex h-16 items-center max-w-[88rem] mx-auto">
          <div className="mr-4 hidden md:flex">
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
          <a
            className="inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 hover:text-accent-foreground h-9 py-2 mr-2 px-0 text-base hover:bg-transparent focus-visible:bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 md:hidden"
            type="button"
            aria-haspopup="dialog"
            aria-expanded="false"
            aria-controls="radix-:rn:"
            data-state="closed"
            href="/"
          >
            <FilePieChart size={26} />
          </a>
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
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="h-4 w-4 dark:text-neutral-500 text-neutral-500 block sm:hidden"
              >
                <path d="M8 12a1 1 0 1 0 2 0a1 1 0 0 0 -2 0"></path>
                <path d="M14 12a1 1 0 1 0 2 0a1 1 0 0 0 -2 0"></path>
                <path d="M15.5 17c0 1 1.5 3 2 3c1.5 0 2.833 -1.667 3.5 -3c.667 -1.667 .5 -5.833 -1.5 -11.5c-1.457 -1.015 -3 -1.34 -4.5 -1.5l-.972 1.923a11.913 11.913 0 0 0 -4.053 0l-.975 -1.923c-1.5 .16 -3.043 .485 -4.5 1.5c-2 5.667 -2.167 9.833 -1.5 11.5c.667 1.333 2 3 3.5 3c.5 0 2 -2 2 -3"></path>
                <path d="M7 16.5c3.5 1 6.5 1 10 0"></path>
              </svg>
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
      <div className="block md:hidden">
        <div className="flex justify-between items-center w-full rounded-md px-4 py-4">
          <a className="flex items-center gap-1.5" href="/">
            Logo
          </a>
          <svg
            stroke="currentColor"
            fill="currentColor"
            strokeWidth="0"
            viewBox="0 0 512 512"
            className="text-black dark:text-white h-6 w-6"
            height="1em"
            width="1em"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M432 176H80c-8.8 0-16-7.2-16-16s7.2-16 16-16h352c8.8 0 16 7.2 16 16s-7.2 16-16 16zM432 272H80c-8.8 0-16-7.2-16-16s7.2-16 16-16h352c8.8 0 16 7.2 16 16s-7.2 16-16 16zM432 368H80c-8.8 0-16-7.2-16-16s7.2-16 16-16h352c8.8 0 16 7.2 16 16s-7.2 16-16 16z"></path>
          </svg>
        </div>
      </div>
    </header>
  );
};

export default Header;
