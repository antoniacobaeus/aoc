const std = @import("std");
const ArrayList = std.ArrayList;
const Allocator = std.mem.Allocator;
const eql = std.mem.eql;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    std.debug.print("Hello, {s}!\n", .{"World"});

    var left = ArrayList(u32).init(allocator);
    var right = ArrayList(u32).init(allocator);

    while (true) {
        const stdin = std.io.getStdIn().reader();
        const bare_line = try stdin.readUntilDelimiterAlloc(
            std.heap.page_allocator,
            '\n',
            8192,
        );

        if (bare_line.len == 0) {
            break;
        }
        std.debug.print("your line {s}\n", .{bare_line});
        defer std.heap.page_allocator.free(bare_line);

        const line = std.mem.trim(u8, bare_line, "\r");

        var it = std.mem.split(u8, line, "   ");

        const left_num = try std.fmt.parseInt(u32, it.next().?, 10);
        try left.append(left_num);
        const right_num = try std.fmt.parseInt(u32, it.next().?, 10);
        try right.append(right_num);
    }

    const x = try left.toOwnedSlice();
    const y = try right.toOwnedSlice();

    std.mem.sort(u32, x, {}, comptime std.sort.asc(u32));
    std.mem.sort(u32, y, {}, comptime std.sort.asc(u32));

    var p1 = @as(u64, 0);
    for (x, 0..) |left_val, i| {
        const right_val = y[i];

        const diff = @abs(@as(i64, right_val) - @as(i64, left_val));
        p1 = p1 + diff;

        std.debug.print("Left: {d}, Right: {d}\n", .{ left_val, right_val });
    }

    var p2 = @as(u64, 0);
    for (x) |left_val| {
        var c = @as(u64, 0);
        for (y) |right_val| {
            if (left_val == right_val) {
                c = c + 1;
            }
        }
        p2 = p2 + left_val * c;
    }

    std.debug.print("p1: {d}\n", .{p1});
    std.debug.print("p2: {d}\n", .{p2});

    // std.mem.sort(u8, &right, std.sort.asc(u8));

}
