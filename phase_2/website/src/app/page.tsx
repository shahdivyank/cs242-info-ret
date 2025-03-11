"use client";
import { columns } from "@/components/columns";
import { DataTable } from "@/components/ui/data-table";
import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";

export default function TaskPage() {
  const [data, setData] = useState([]);

  const [input, setInput] = useState("");
  const [location, setLocation] = useState("");
  const [size, setSize] = useState("5");

  const query = async () => {
    console.log(input, size);

    const response = await fetch(
      `/api/query?q=${input}&size=${size}&location=${location}`
    );

    const data = await response.json();

    setData(data);
  };

  useEffect(() => {
    query();
  }, []);

  const sizes = [5, 10, 15, 20, 25, 50, 75, 100];

  return (
    <>
      <div className="hidden h-full flex-1 flex-col space-y-8 p-8 md:flex">
        <div className="flex items-center justify-between space-y-2">
          <div className="w-full">
            <h2 className="text-2xl font-bold tracking-tight">
              Welcome to TechJobFinder!
            </h2>
            <div className="flex justify-between w-full mt-8">
              <div className="flex gap-4">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Search for job listings..."
                />
                <Input
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  placeholder="Enter location..."
                />

                <Select value={size} onValueChange={(value) => setSize(value)}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="5" />
                  </SelectTrigger>
                  <SelectContent>
                    {sizes.map((size, index) => (
                      <SelectItem key={index} value={String(size)}>
                        {size}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <Button variant="default" onClick={query}>
                Search
              </Button>
            </div>
          </div>
        </div>
        <DataTable data={data} columns={columns} />
      </div>
    </>
  );
}
