"use client";

import { SquareArrowOutUpRight } from "lucide-react";
import Link from "next/link";

export const columns: any = [
  {
    accessorKey: "metadata.title",
    header: "Title",
    cell: ({ row, getValue }: any) => (
      <div
        onClick={row.getToggleSelectedHandler()}
        className="hover:cursor-pointer"
      >
        {getValue()}
      </div>
    ),
  },
  {
    accessorKey: "metadata.location",
    header: "Location",
    cell: ({ row, getValue }: any) => (
      <div
        onClick={row.getToggleSelectedHandler()}
        className="hover:cursor-pointer"
      >
        {getValue()}
      </div>
    ),
  },
  {
    accessorKey: "page_content",
    header: "Description",
    cell: ({ row, getValue }: any) => (
      <div
        onClick={row.getToggleSelectedHandler()}
        className="hover:cursor-pointer"
      >
        {getValue()}
      </div>
    ),
  },
  {
    accessorKey: "score",
    header: "Score",
    cell: ({ row, getValue }: any) => (
      <div
        onClick={row.getToggleSelectedHandler()}
        className="hover:cursor-pointer"
      >
        {getValue()}
      </div>
    ),
  },
  {
    accessorKey: "metadata.link",
    header: "Application Link",
    cell: ({ row, getValue }: any) => (
      <div
        onClick={row.getToggleSelectedHandler()}
        className="hover:cursor-pointer"
      >
        <Link href={getValue()} target="_blank">
          <SquareArrowOutUpRight />
        </Link>
      </div>
    ),
  },
];
