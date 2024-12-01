const std = @import("std");

fn parseInput(data: []u8) !struct { []u32, []u32 } {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();

    var left = std.ArrayList(u32).init(allocator);
    var right = std.ArrayList(u32).init(allocator);

    var line_it = std.mem.split(u8, data, "\n");

    while (line_it.next()) |line| {
        if (line.len == 0) {
            continue;
        }
        var it = std.mem.split(u8, line, "   ");
        const l = try std.fmt.parseInt(u32, it.next().?, 10);
        const r = try std.fmt.parseInt(u32, it.next().?, 10);
        try left.append(l);
        try right.append(r);
    }
    const x = try left.toOwnedSlice();
    const y = try right.toOwnedSlice();

    std.mem.sort(u32, x, {}, comptime std.sort.asc(u32));
    std.mem.sort(u32, y, {}, comptime std.sort.asc(u32));

    return .{ x, y };
}

fn part1(left: []u32, right: []u32) u64 {
    var res: u64 = 0;
    for (left, right) |l, r| {
        const diff = @abs(@as(i64, r) - @as(i64, l));
        res = res + diff;
    }
    return res;
}

fn part2(left: []u32, right: []u32) u64 {
    var res: u64 = 0;
    for (left) |l| {
        var c: u64 = 0;
        for (right) |r| {
            if (l == r) {
                c = c + 1;
            }
        }
        res = res + l * c;
    }
    return res;
}

pub fn main() !void {
    const data = @embedFile("input/2024/01.txt");

    const left, const right = try parseInput(@constCast(data));

    const p1 = part1(left, right);
    const p2 = part2(left, right);

    std.debug.print("p1: {d}\n", .{p1});
    std.debug.print("p2: {d}\n", .{p2});
}
