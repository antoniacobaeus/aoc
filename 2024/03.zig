const std = @import("std");

const Mul = struct {
    a: i64,
    b: i64,
    pub fn format(
        self: Mul,
        comptime fmt: []const u8,
        options: std.fmt.FormatOptions,
        writer: anytype,
    ) !void {
        _ = fmt;
        _ = options;

        try writer.print("({d} {d})\n", .{ self.a, self.b });
    }
};

fn preProcess(data: []u8) ![]Mul {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();

    var muls = std.ArrayList(Mul).init(allocator);

    var it_do = std.mem.split(u8, data, "do()");
    while (it_do.next()) |do_line| {
        var it_dont = std.mem.split(u8, do_line, "don\'t()");
        // everything between do and dont is enabled
        if (it_dont.peek() != null) {
            for (try parseInput(@constCast(it_dont.next().?))) |mul| {
                try muls.append(mul);
            }
        }
    }
    return muls.items;
}

fn parseInput(data: []u8) ![]Mul {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();

    var muls = std.ArrayList(Mul).init(allocator);

    var line_it = std.mem.split(u8, data, "\n");

    while (line_it.next()) |line| {
        if (line.len == 0) {
            continue;
        }

        var it = std.mem.split(u8, line, "mul(");

        while (it.next()) |m| {
            var it_2 = std.mem.split(u8, m, ")");
            const m2 = it_2.next().?;
            if (!std.mem.containsAtLeast(u8, m2, 1, ",")) {
                continue;
            }

            var it_3 = std.mem.split(u8, m2, ",");
            const a1 = it_3.next().?;
            const b1 = it_3.next().?;
            if (it_3.peek() != null) {
                continue;
            }
            const a = std.fmt.parseInt(i64, a1, 10) catch {
                continue;
            };
            const b = std.fmt.parseInt(i64, b1, 10) catch {
                continue;
            };
            try muls.append(Mul{ .a = a, .b = b });
        }
    }

    return muls.items;
}

fn part1(data: []u8) !i128 {
    const muls = try parseInput(data);

    var res: i128 = 0;
    for (muls) |mul| {
        res += mul.a * mul.b;
    }
    return res;
}

fn part2(data: []u8) !i128 {
    const muls = try preProcess(data);

    var res: i128 = 0;
    for (muls) |mul| {
        res += mul.a * mul.b;
    }

    return res;
}

pub fn main() !void {
    const data = @embedFile("input/2024/03.txt");

    var t1 = std.time.nanoTimestamp();
    const p1 = try part1(@constCast(data));
    std.debug.print("p1: {d} in {d}s\n", .{ p1, @as(f128, @floatFromInt(std.time.nanoTimestamp() - t1)) / 10e9 });

    t1 = std.time.nanoTimestamp();
    const p2 = try part2(@constCast(data));
    std.debug.print("p2: {d} in {d}s\n", .{ p2, @as(f128, @floatFromInt(std.time.nanoTimestamp() - t1)) / 10e9 });
}
