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
import { Person, makeData } from '../services/reports';
import { LucideSearch } from 'lucide-react';
import { Input } from './ui/input';

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
  const rerender = useReducer(() => ({}), {})[1];

  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [globalFilter, setGlobalFilter] = useState('');

  const columns = useMemo<ColumnDef<Person, any>[]>(
    () => [
      {
        accessorKey: 'id',
        filterFn: 'equalsString', //note: normal non-fuzzy filter column - exact match required
      },
      {
        accessorKey: 'firstName',
        cell: (info) => info.getValue(),
        filterFn: 'includesStringSensitive', //note: normal non-fuzzy filter column
      },
      {
        accessorFn: (row) => row.lastName, //note: normal non-fuzzy filter column - case sensitive
        id: 'lastName',
        cell: (info) => info.getValue(),
        header: () => <span>Last Name</span>,
        filterFn: 'includesString', //note: normal non-fuzzy filter column - case insensitive
      },
      {
        accessorFn: (row) => `${row.firstName} ${row.lastName}`,
        id: 'fullName',
        header: 'Full Name',
        cell: (info) => info.getValue(),
        filterFn: 'fuzzy', //using our custom fuzzy filter function
        // filterFn: fuzzyFilter, //or just define with the function
        sortingFn: fuzzySort, //sort by fuzzy rank (falls back to alphanumeric)
      },
    ],
    []
  );

  const [data, setData] = useState<Person[]>(() => makeData(5_000));
  const refreshData = () => setData((_old) => makeData(50_000)); //stress test

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

  return (
    <div className="p-2 my-8 shadow-sm border rounded-lg overflow-x-auto bg-gray-50">
      <div className="flex items-center justify-between">
        <div className="">Тут еще всякие быстрые фильтры</div>
        <div className="flex justify-end py-2">
          <DebouncedInput
            value={globalFilter ?? ''}
            onChange={(value) => setGlobalFilter(String(value))}
            className=" font-lg shadow border border-block"
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
                <tr key={row.id}>
                  {row.getVisibleCells().map((cell) => {
                    return (
                      <td key={cell.id} className="px-6 py-4 whitespace-nowrap">
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <div className="h-2" />
      <div className="flex items-center gap-2">
        <button
          className="border rounded p-1"
          onClick={() => table.setPageIndex(0)}
          disabled={!table.getCanPreviousPage()}
        >
          {'<<'}
        </button>
        <button
          className="border rounded p-1"
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          {'<'}
        </button>
        <button
          className="border rounded p-1"
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          {'>'}
        </button>
        <button
          className="border rounded p-1"
          onClick={() => table.setPageIndex(table.getPageCount() - 1)}
          disabled={!table.getCanNextPage()}
        >
          {'>>'}
        </button>
        <span className="flex items-center gap-1">
          <div>Page</div>
          <strong>
            {table.getState().pagination.pageIndex + 1} of{' '}
            {table.getPageCount()}
          </strong>
        </span>
        <span className="flex items-center gap-1">
          | Go to page:
          <input
            type="number"
            defaultValue={table.getState().pagination.pageIndex + 1}
            onChange={(e) => {
              const page = e.target.value ? Number(e.target.value) - 1 : 0;
              table.setPageIndex(page);
            }}
            className="border p-1 rounded w-16"
          />
        </span>
        <select
          value={table.getState().pagination.pageSize}
          onChange={(e) => {
            table.setPageSize(Number(e.target.value));
          }}
        >
          {[10, 20, 30, 40, 50].map((pageSize) => (
            <option key={pageSize} value={pageSize}>
              Show {pageSize}
            </option>
          ))}
        </select>
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
        className="sm:flex w-full relative hidden justify-start items-center text-sm text-muted-foreground py-2 outline-none border border-transparent shadow-[0px_2px_3px_-1px_rgba(0,0,0,0.1),0px_1px_0px_0px_rgba(25,28,33,0.02),0px_0px_0px_1px_rgba(25,28,33,0.08)] px-8 rounded-xl bg-white"
      />
      <LucideSearch
        className="absolute left-2 top-1/2 z-10 -translate-y-1/2"
        size={16}
      />
    </label>
  );
}
