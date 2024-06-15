import {
  Column,
  ColumnDef,
  ColumnFiltersState,
  FilterFn,
  SortingFn,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  sortingFns,
  useReactTable,
} from '@tanstack/react-table';
import { getReportsApi } from '@/api/report';
import { useQuery } from '@tanstack/react-query';

// A TanStack fork of Kent C. Dodds' match-sorter library that provides ranking information
import {
  RankingInfo,
  rankItem,
  compareItems,
} from '@tanstack/match-sorter-utils';
import {
  useReducer,
  useState,
  useMemo,
  useEffect,
  InputHTMLAttributes,
} from 'react';
import {
  LucideArrowLeftCircle,
  LucideArrowRightCircle,
  LucideSearch,
} from 'lucide-react';
import { Input } from './ui/input';
import { IconFidgetSpinner } from '@tabler/icons-react';
import { Link } from 'react-router-dom';

declare module '@tanstack/react-table' {
  //add fuzzy filter to the filterFns
  interface FilterFns {
    fuzzy: FilterFn<unknown>;
  }
  interface FilterMeta {
    itemRank: RankingInfo;
  }
}

// Define a custom fuzzy filter function that will apply ranking info to rows (using match-sorter utils)
const fuzzyFilter: FilterFn<any> = (row, columnId, value, addMeta) => {
  // Rank the item
  const itemRank = rankItem(row.getValue(columnId), value);

  // Store the itemRank info
  addMeta({
    itemRank,
  });

  // Return if the item should be filtered in/out
  return itemRank.passed;
};

// Define a custom fuzzy sort function that will sort by rank if the row has ranking information
const fuzzySort: SortingFn<any> = (rowA, rowB, columnId) => {
  let dir = 0;

  // Only sort by rank if the column has ranking information
  if (rowA.columnFiltersMeta[columnId]) {
    dir = compareItems(
      rowA.columnFiltersMeta[columnId]?.itemRank!,
      rowB.columnFiltersMeta[columnId]?.itemRank!
    );
  }

  // Provide an alphanumeric fallback for when the item ranks are equal
  return dir === 0 ? sortingFns.alphanumeric(rowA, rowB, columnId) : dir;
};

export function ReportsTable() {
  const [page, setPage] = useState(1);
  const { data: reportsData, isLoading: reportsDataLoading } = useQuery({
    queryKey: ['reports', page],
    queryFn: async () => {
      return getReportsApi({ page });
    },
  });

  const rerender = useReducer(() => ({}), {})[1];

  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [globalFilter, setGlobalFilter] = useState('');

  const columns = useMemo<ColumnDef<any, any>[]>(
    () => [
      {
        accessorKey: 'id',
        header: () => <span>#</span>,
        filterFn: 'equalsString', //note: normal non-fuzzy filter column - exact match required
      },
      {
        accessorKey: 'search_query',
        header: () => <span>Запрос</span>,
        cell: (info) => info.getValue(),
        filterFn: 'fuzzy', //note: normal non-fuzzy filter column
        sortingFn: fuzzySort, //sort by fuzzy rank (falls back to alphanumeric)
      },
      {
        accessorKey: 'date',
        header: () => <span>Дата</span>,
        cell: (info) =>
          new Intl.DateTimeFormat('ru-RU').format(new Date(info.getValue())),
        filterFn: 'fuzzy', //note: normal non-fuzzy filter column
        sortingFn: fuzzySort, //sort by fuzzy rank (falls back to alphanumeric)
      },
      {
        accessorKey: 'status',
        header: () => <span>Статус</span>,
        cell: (info) => {
          console.log({ info });
          const isReady =
            (
              info.row?.original?.blocks?.filter(
                (v) => v?.readiness === 'ready'
              ) || []
            ).length > 0;
          return <div>{isReady ? 'Готов' : 'В процессе'}</div>;
        },
        filterFn: 'fuzzy', //note: normal non-fuzzy filter column
        sortingFn: fuzzySort, //sort by fuzzy rank (falls back to alphanumeric)
      },
    ],
    []
  );

  const [data, setData] = useState<any[]>([]);

  console.log({ data });

  useEffect(() => {
    if (reportsData?.results?.length) {
      setData(reportsData.results);
    }
  }, [reportsData]);

  const table = useReactTable({
    data,
    columns,
    filterFns: {
      fuzzy: fuzzyFilter, //define as a filter function that can be used in column definitions
    },
    state: {
      columnFilters,
      globalFilter,
    },
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    globalFilterFn: 'fuzzy', //apply fuzzy filter to the global filter (most common use case for fuzzy filter)
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(), //client side filtering
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    debugTable: true,
    debugHeaders: true,
    debugColumns: false,
  });

  //apply the fuzzy sort if the fullName column is being filtered
  useEffect(() => {
    if (table.getState().columnFilters[0]?.id === 'fullName') {
      if (table.getState().sorting[0]?.id !== 'fullName') {
        table.setSorting([{ id: 'fullName', desc: false }]);
      }
    }
  }, [table.getState().columnFilters[0]?.id]);

  if (reportsDataLoading) {
    return (
      <div>
        <IconFidgetSpinner className=" animate-spin" />
      </div>
    );
  }

  return (
    <div className="p-2 my-8 shadow-sm border rounded-lg overflow-x-auto bg-gray-50">
      <div className="flex items-center justify-between">
        <div className="flex justify-end py-2 w-[360px]">
          <DebouncedInput
            value={globalFilter ?? ''}
            onChange={(value) => setGlobalFilter(String(value))}
            className="font-lg shadow border border-block"
            placeholder="Поиск по всем параметрам..."
          />
        </div>
      </div>
      <div className="h-2" />
      <div className="border rounded-lg">
        <table className="w-full table-auto text-sm text-left ">
          <thead className="bg-gray-50 text-gray-600 font-medium border-b">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <th
                      key={header.id}
                      colSpan={header.colSpan}
                      className="py-3 px-6"
                    >
                      {header.isPlaceholder ? null : (
                        <>
                          <div
                            {...{
                              className: header.column.getCanSort()
                                ? 'cursor-pointer select-none'
                                : '',
                              onClick: header.column.getToggleSortingHandler(),
                            }}
                          >
                            {flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                            {{
                              asc: ' 🔼',
                              desc: ' 🔽',
                            }[header.column.getIsSorted() as string] ?? null}
                          </div>
                        </>
                      )}
                    </th>
                  );
                })}
              </tr>
            ))}
          </thead>
          <tbody className="text-gray-600 divide-y">
            {table.getRowModel().rows.map((row) => {
              return (
                <tr key={row.id} className="hover:bg-gray-400/10">
                  <Link
                    to={`/reports/${row.original?.id}`}
                    className="contents hover:bg-black"
                  >
                    {row.getVisibleCells().map((cell) => {
                      return (
                        <td
                          key={cell.id}
                          className="px-6 py-4 whitespace-nowrap"
                        >
                          {flexRender(
                            cell.column.columnDef.cell,
                            cell.getContext()
                          )}
                        </td>
                      );
                    })}
                  </Link>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <div className="h-2" />
      <div className="flex items-center gap-2">
        <button
          className="border rounded p-1 disabled:text-gray-300 text-gray-700"
          onClick={() => {
            // table.previousPage();
            if (reportsData.previous) {
              setPage((page) => page - 1);
            }
          }}
          disabled={!reportsData.previous}
        >
          <LucideArrowLeftCircle />
        </button>
        <button
          className="border rounded p-1 disabled:text-gray-300 text-gray-700"
          onClick={() => {
            // table.nextPage();
            if (reportsData.next) {
              setPage((page) => page + 1);
            }
          }}
          disabled={!reportsData.next}
        >
          <LucideArrowRightCircle />
        </button>
        <span className="flex items-center gap-1">
          <div>Страница</div>
          <strong>
            {page} из {Math.ceil(reportsData?.count / 10)}
          </strong>
        </span>
      </div>
    </div>
  );
}

function Filter({ column }: { column: Column<any, unknown> }) {
  const columnFilterValue = column.getFilterValue();

  return (
    <DebouncedInput
      type="text"
      value={(columnFilterValue ?? '') as string}
      onChange={(value) => column.setFilterValue(value)}
      placeholder={`Search...`}
      className="w-36 border shadow rounded"
    />
  );
}

// A typical debounced input react component
export function DebouncedInput({
  value: initialValue,
  onChange,
  debounce = 500,
  ...props
}: {
  value: string | number;
  onChange: (value: string | number) => void;
  debounce?: number;
} & Omit<InputHTMLAttributes<HTMLInputElement>, 'onChange'>) {
  const [value, setValue] = useState(initialValue);

  useEffect(() => {
    setValue(initialValue);
  }, [initialValue]);

  useEffect(() => {
    const timeout = setTimeout(() => {
      onChange(value);
    }, debounce);

    return () => clearTimeout(timeout);
  }, [value]);

  return (
    <label className="relative flex w-full">
      <Input
        {...props}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="px-8"
      />
      <LucideSearch
        className="absolute left-2 top-1/2 z-10 -translate-y-1/2"
        size={16}
      />
    </label>
  );
}
