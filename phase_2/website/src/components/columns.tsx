"use client";
export const columns: any = [
  {
    accessorKey: "metadata",
    header: "Title",
    cell: ({ row, getValue }: any) => (
      <div
        onClick={row.getToggleSelectedHandler()}
        className="hover:cursor-pointer"
      >
        hello
        {/* {getValue().title} */}
      </div>
    ),
  },
  {
    accessorKey: "metadata",
    header: "Location",
    cell: ({ row, getValue }: any) => (
      <div
        onClick={row.getToggleSelectedHandler()}
        className="hover:cursor-pointer"
      >
        hello
        {/* {getValue().location} */}
      </div>
    ),
  },
];
