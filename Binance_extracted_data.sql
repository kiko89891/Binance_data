USE [Binance_data]
GO

/****** Object:  Table [dbo].[BTCUSDT_order_book]    Script Date: 03/03/2024 23:33:35 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[BTCUSDT_order_book](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[bid_price] [float] NULL,
	[ask_price] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

