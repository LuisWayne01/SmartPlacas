using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite("Data Source=placas.db"));

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}

// Lê a placa física
app.MapGet("/p/{id}", async (string id, AppDbContext db) =>
{
    var placa = await db.Placas.FindAsync(id.ToUpper());
    if (placa == null) return Results.NotFound("Placa inválida.");
    
    if (!string.IsNullOrEmpty(placa.UrlDestino)) 
        return Results.Redirect(placa.UrlDestino);
        
    return Results.Ok($"A placa {id} é VIRGEM. Pronta para ativação.");
});

// Gera estoque na gráfica
app.MapPost("/api/placas/gerar", async (int qtd, AppDbContext db) =>
{
    var novas = Enumerable.Range(0, qtd)
        .Select(_ => new Placa { Id = Guid.NewGuid().ToString("N").Substring(0, 6).ToUpper() })
        .ToList();
        
    db.Placas.AddRange(novas);
    await db.SaveChangesAsync();
    return Results.Ok(novas);
});

// Ativa a placa na hora da venda
app.MapPut("/api/placas/ativar/{id}", async (string id, NovaPlacaDto dto, AppDbContext db) =>
{
    var placa = await db.Placas.FindAsync(id.ToUpper());
    if (placa == null) return Results.NotFound("Placa não encontrada.");
    
    placa.UrlDestino = dto.Url;
    await db.SaveChangesAsync();
    return Results.Ok(placa);
});

app.Run();

// Modelos
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
    public DbSet<Placa> Placas => Set<Placa>();
}

public class Placa
{
    public string Id { get; set; } = string.Empty;
    public string? UrlDestino { get; set; }
}

public class NovaPlacaDto 
{ 
    public string Url { get; set; } = string.Empty; 
}