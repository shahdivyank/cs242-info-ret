import { Metadata } from "next";
import { columns } from "@/components/columns";
import { DataTable } from "@/components/ui/data-table";
import { tasks } from "@/data/tasks";

export const metadata: Metadata = {
  title: "Tasks",
  description: "A task and issue tracker build using Tanstack Table.",
};

export default async function TaskPage() {
  return (
    <>
      <div className="hidden h-full flex-1 flex-col space-y-8 p-8 md:flex">
        <div className="flex items-center justify-between space-y-2">
          <div>
            <h2 className="text-2xl font-bold tracking-tight">
              Welcome to TechJobFinder!
            </h2>
            <p className="text-muted-foreground">Relevant Job Postings</p>
          </div>
        </div>
        <DataTable data={tasks} columns={columns} />
      </div>
    </>
  );
}
