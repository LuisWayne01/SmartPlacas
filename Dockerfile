# Usa a imagem oficial do SDK do .NET para compilar
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

# Copia os arquivos e compila o projeto
COPY . ./
RUN dotnet publish -c Release -o out

# Usa a imagem mais leve do .NET para rodar (sem o peso do SDK)
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/out .

# Configura a porta que o Render vai usar (por padrão, porta 8080)
EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080

# Comando para iniciar a API
ENTRYPOINT ["dotnet", "SmartPlacas.dll"]