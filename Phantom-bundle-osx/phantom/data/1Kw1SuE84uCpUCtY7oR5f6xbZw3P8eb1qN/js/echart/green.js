var theme = {

                    color: [
                        '#e70b3b', '#595959', '#c7c7c7', '#d9d9d9',
                        '#a6a6a6', '#8c8c8c', '#737373', '#d9d9d9'
                    ],

                    title: {
                        itemGap: 8,
                        textStyle: {
                            fontWeight: 'normal',
                            color: '#878787'
                        }
                    },

                    dataRange: {
                        color: ['#616161', '#b5b5b5']
                    },

                    toolbox: {
                        color: ['#878787', '#878787', '#878787', '#878787']
                    },

                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.5)',
                        axisPointer: {
                            type: 'line',
                            lineStyle: {
                                color: '#878787',
                                type: 'dashed'
                            },
                            crossStyle: {
                                color: '#878787'
                            },
                            shadowStyle: {
                                color: 'rgba(200,200,200,0.3)'
                            }
                        }
                    },

                    dataZoom: {
                        dataBackgroundColor: '#eee',
                        fillerColor: 'rgba(135,135,135,0.2)',
                        handleColor: '#878787'
                    },
                    grid: {
                        borderWidth: 0
                    },

                    categoryAxis: {
                        axisLine: {
                            lineStyle: {
                                color: '#878787'
                            }
                        },
                        splitLine: {
                            lineStyle: {
                                color: ['#eee']
                            }
                        }
                    },

                    valueAxis: {
                        axisLine: {
                            lineStyle: {
                                color: '#878787'
                            }
                        },
                        splitArea: {
                            show: true,
                            areaStyle: {
                                color: ['rgba(250,250,250,0.1)', 'rgba(200,200,200,0.1)']
                            }
                        },
                        splitLine: {
                            lineStyle: {
                                color: ['#eee']
                            }
                        }
                    },
                    timeline: {
                        lineStyle: {
                            color: '#878787'
                        },
                        controlStyle: {
                            normal: {color: '#878787'},
                            emphasis: {color: '#878787'}
                        }
                    },

                    k: {
                        itemStyle: {
                            normal: {
                                color: '#a6a6a6',
                                color0: '#cccccc',
                                lineStyle: {
                                    width: 1,
                                    color: '#878787',
                                    color0: '#b3b3b3'
                                }
                            }
                        }
                    },
                    map: {
                        itemStyle: {
                            normal: {
                                areaStyle: {
                                    color: '#ddd'
                                },
                                label: {
                                    textStyle: {
                                        color: '#232323'
                                    }
                                }
                            },
                            emphasis: {
                                areaStyle: {
                                    color: '#e70b3b'
                                },
                                label: {
                                    textStyle: {
                                        color: '#232323'
                                    }
                                }
                            }
                        }
                    },
                    force: {
                        itemStyle: {
                            normal: {
                                linkStyle: {
                                    strokeColor: '#408829'
                                }
                            }
                        }
                    },
                    chord: {
                        padding: 4,
                        itemStyle: {
                            normal: {
                                lineStyle: {
                                    width: 1,
                                    color: 'rgba(128, 128, 128, 0.5)'
                                },
                                chordStyle: {
                                    lineStyle: {
                                        width: 1,
                                        color: 'rgba(128, 128, 128, 0.5)'
                                    }
                                }
                            },
                            emphasis: {
                                lineStyle: {
                                    width: 1,
                                    color: 'rgba(128, 128, 128, 0.5)'
                                },
                                chordStyle: {
                                    lineStyle: {
                                        width: 1,
                                        color: 'rgba(128, 128, 128, 0.5)'
                                    }
                                }
                            }
                        }
                    },
                    gauge: {
                        startAngle: 225,
                        endAngle: -45,
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: [[0.2, '#b3b3b3'], [0.8, '#a6a6a6'], [1, '#878787']],
                                width: 8
                            }
                        },
                        axisTick: {
                            splitNumber: 10,
                            length: 12,
                            lineStyle: {
                                color: 'auto'
                            }
                        },
                        axisLabel: {
                            textStyle: {
                                color: 'auto'
                            }
                        },
                        splitLine: {
                            length: 18,
                            lineStyle: {
                                color: 'auto'
                            }
                        },
                        pointer: {
                            length: '90%',
                            color: 'auto'
                        },
                        title: {
                            textStyle: {
                                color: '#333'
                            }
                        },
                        detail: {
                            textStyle: {
                                color: 'auto'
                            }
                        }
                    },
                    textStyle: {
                        fontFamily: 'Arial, Verdana, sans-serif'
                    }
                }
